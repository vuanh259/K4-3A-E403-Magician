import asyncio
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import discord
from discord import app_commands
from discord.ext import commands

from ai import analyze_messages
from config import settings
from reminders import ReminderService
from storage import Store
from ui import build_summary_embed, build_tasks_embed


store = Store(settings.db_path)


def now_local():
    return datetime.now(ZoneInfo(settings.timezone))


async def collect_messages(channels: list[discord.TextChannel]) -> list[dict]:
    rows = []

    # Chỉ đọc message trong 24 giờ gần nhất
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)

    for channel in channels:
        try:
            async for msg in channel.history(
                limit=settings.message_limit_per_channel,
                after=cutoff_time,
                oldest_first=False,
            ):
                # Bỏ qua message của bot
                if msg.author.bot:
                    continue

                content = (msg.content or "").strip()

                # Bỏ qua message rỗng
                if not content:
                    continue

                rows.append({
                    "message_id": str(msg.id),
                    "channel_id": str(channel.id),
                    "channel_name": channel.name,
                    "author": msg.author.display_name,
                    "created_at": msg.created_at.isoformat(),
                    "content": content[:1800],
                    "jump_url": msg.jump_url,
                })

        except (discord.Forbidden, discord.HTTPException):
            continue

    # Sắp xếp từ cũ -> mới
    rows.sort(key=lambda x: x["created_at"])

    return rows


class ChannelPicker(discord.ui.ChannelSelect):
    def __init__(self, owner_id: int):
        self.owner_id = owner_id

        super().__init__(
            placeholder="Tick các channel muốn tổng hợp...",
            min_values=1,
            max_values=settings.max_channels_per_summary,
            channel_types=[discord.ChannelType.text],
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Bộ chọn này thuộc về user khác.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(
            ephemeral=True,
            thinking=True,
        )

        selected = []

        for v in self.values:
            ch = (
                interaction.guild.get_channel(v.id)
                if interaction.guild
                else None
            )

            if isinstance(ch, discord.TextChannel):
                selected.append(ch)

        if not selected:
            await interaction.followup.send(
                "Không có text channel hợp lệ.",
                ephemeral=True,
            )
            return

        await run_summary(
            interaction,
            selected,
        )


class SummaryView(discord.ui.View):
    def __init__(self, owner_id: int):
        super().__init__(timeout=180)

        self.owner_id = owner_id

        self.add_item(
            ChannelPicker(owner_id)
        )

    @discord.ui.button(
        label="Quét tất cả channel khả dụng",
        emoji="🧭",
        style=discord.ButtonStyle.secondary,
    )
    async def all_channels(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message(
                "Nút này thuộc về user khác.",
                ephemeral=True,
            )
            return

        if not interaction.guild:
            await interaction.response.send_message(
                "Hãy dùng lệnh trong server.",
                ephemeral=True,
            )
            return

        await interaction.response.defer(
            ephemeral=True,
            thinking=True,
        )

        me = interaction.guild.me

        channels = []

        for ch in interaction.guild.text_channels:
            perms = ch.permissions_for(me)

            if (
                perms.view_channel
                and perms.read_message_history
            ):
                channels.append(ch)

        channels = channels[
            :settings.max_channels_per_summary
        ]

        if not channels:
            await interaction.followup.send(
                "Bot chưa có quyền đọc channel nào.",
                ephemeral=True,
            )
            return

        await run_summary(
            interaction,
            channels,
        )


async def run_summary(
    interaction: discord.Interaction,
    channels: list[discord.TextChannel],
):
    names = [
        c.name
        for c in channels
    ]

    await interaction.followup.send(
        "🔎 Đang quét message trong 24 giờ gần nhất: "
        + ", ".join(
            f"`#{n}`"
            for n in names
        ),
        ephemeral=True,
    )

    messages = await collect_messages(
        channels
    )

    if not messages:
        await interaction.followup.send(
            "Không tìm thấy message nào trong 24 giờ gần nhất.\n"
            "Hoặc bot chưa có quyền View Channel / Read Message History / Message Content Intent.",
            ephemeral=True,
        )
        return

    print(
        f"[SUMMARY] Found {len(messages)} messages "
        f"from {len(channels)} channels: {', '.join(f'#{n}' for n in names)}"
    )
    print(f"[AI] Đang gửi {len(messages)} tin nhắn sang AI ({settings.ai_model}) để trích xuất...")

    result = await analyze_messages(
        messages=messages,
        current_time_iso=now_local().isoformat(),
        timezone_name=settings.timezone,
    )

    items = [
        x
        for x in result.get("items", [])
        if (
            x.get("action_required") is True
            or x.get("type")
            in {
                "assignment",
                "deadline",
                "meeting",
                "schedule_change",
            }
        )
    ]

    print(f"[AI] Phân tích hoàn tất! Trích xuất được {len(items)} việc quan trọng:")
    for i, it in enumerate(items, 1):
        prio = str(it.get("priority", "medium")).upper()
        dl = it.get("deadline_iso") or "Không có"
        src_msg = msg_map.get(str(it.get("source_message_id")))
        ch = getattr(getattr(src_msg, "channel", None), "name", "unknown")
        print(f"   {i}. [{prio}] {it.get('title')} | Hạn: {dl} | Nguồn: #{ch}")

    task_ids = await store.upsert_items(
        user_id=interaction.user.id,
        guild_id=(
            interaction.guild.id
            if interaction.guild
            else None
        ),
        items=items,
    )

    await store.save_summary_run(
        user_id=interaction.user.id,
        guild_id=(
            interaction.guild.id
            if interaction.guild
            else None
        ),
        channels=names,
        message_count=len(messages),
        item_count=len(items),
    )

    embed = build_summary_embed(
        items,
        task_ids,
        names,
        len(messages),
    )

    await interaction.channel.send(
        content=(
            f"{interaction.user.mention} "
            "đây là summary bạn vừa yêu cầu:"
        ),
        embed=embed,
    )

    channel_title = getattr(interaction.channel, "name", "channel")
    print(f"[DISCORD] Đã gửi bản tin Embed tới #{channel_title} cho {interaction.user.name} thành công!")

    await interaction.followup.send(
        f"✅ Xong. Đã phân tích **{len(messages)} message** "
        f"trong 24 giờ gần nhất và lưu **{len(items)} item** "
        "để theo dõi / DM reminder.",
        ephemeral=True,
    )


class ProductBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()

        intents.message_content = True

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

        self.reminder_service = ReminderService(
            self,
            store,
        )

    async def setup_hook(self):
        await store.init()

        if settings.discord_guild_id:
            guild = discord.Object(
                id=settings.discord_guild_id
            )

            self.tree.copy_global_to(
                guild=guild
            )

            await self.tree.sync(
                guild=guild
            )

            print(
                "Synced slash commands to guild",
                settings.discord_guild_id,
            )

        else:
            await self.tree.sync()

            print(
                "Synced global slash commands"
            )

    async def on_ready(self):
        print(
            f"Logged in as {self.user} "
            f"({self.user.id})"
        )

        self.reminder_service.start()


bot = ProductBot()


@bot.tree.command(
    name="summary",
    description="Chọn channel rồi AI tổng hợp task, deadline và thay đổi lịch.",
)
async def summary(
    interaction: discord.Interaction,
):
    if not interaction.guild:
        await interaction.response.send_message(
            "Hãy dùng /summary trong server.",
            ephemeral=True,
        )
        return

    await interaction.response.send_message(
        "### Chọn channel muốn tổng hợp\n"
        "Tick một hoặc nhiều channel.\n"
        "Bot chỉ đọc channel mà bot có quyền và chỉ xét message trong **24 giờ gần nhất**.",
        view=SummaryView(
            interaction.user.id
        ),
        ephemeral=True,
    )


@bot.tree.command(
    name="tasks",
    description="Xem các việc AI đang theo dõi cho bạn.",
)
async def tasks(
    interaction: discord.Interaction,
):
    rows = await store.list_open_tasks(
        interaction.user.id
    )

    await interaction.response.send_message(
        embed=build_tasks_embed(rows),
        ephemeral=True,
    )


@bot.tree.command(
    name="done",
    description="Đánh dấu một task đã hoàn thành.",
)
@app_commands.describe(
    task_id="Task ID hiển thị trong /summary hoặc /tasks"
)
async def done(
    interaction: discord.Interaction,
    task_id: int,
):
    ok = await store.mark_done(
        task_id,
        interaction.user.id,
    )

    await interaction.response.send_message(
        (
            "✅ Đã đánh dấu hoàn thành."
            if ok
            else "Không tìm thấy task của bạn."
        ),
        ephemeral=True,
    )


@bot.tree.command(
    name="correct",
    description="Sửa deadline/priority/title nếu AI hiểu sai.",
)
@app_commands.describe(
    task_id="Task ID",
    deadline_iso=(
        "Deadline ISO-8601, ví dụ "
        "2026-09-17T21:00:00+07:00; "
        "để trống nếu không sửa"
    ),
    priority="high / medium / low",
    title="Tiêu đề mới nếu cần",
)
async def correct(
    interaction: discord.Interaction,
    task_id: int,
    deadline_iso: str | None = None,
    priority: str | None = None,
    title: str | None = None,
):
    if (
        priority is not None
        and priority
        not in {
            "high",
            "medium",
            "low",
        }
    ):
        await interaction.response.send_message(
            "priority phải là high / medium / low.",
            ephemeral=True,
        )
        return

    ok = await store.correct_task(
        task_id,
        interaction.user.id,
        deadline_iso,
        priority,
        title,
    )

    await interaction.response.send_message(
        (
            "✏️ Đã cập nhật. Reminder sẽ được tính lại nếu deadline thay đổi."
            if ok
            else "Không có thay đổi hoặc không tìm thấy task."
        ),
        ephemeral=True,
    )


@bot.tree.command(
    name="test_reminder",
    description="Demo DM reminder cho video CP3.",
)
@app_commands.describe(
    seconds="Chờ bao nhiêu giây trước khi DM"
)
async def test_reminder(
    interaction: discord.Interaction,
    seconds: app_commands.Range[
        int,
        3,
        60,
    ] = 6,
):
    await interaction.response.send_message(
        f"Bot sẽ DM sau {seconds} giây.",
        ephemeral=True,
    )

    await asyncio.sleep(
        seconds
    )

    try:
        await interaction.user.send(
            "⏰ **DEADLINE REMINDER — DEMO**\n"
            "Lab 5 còn 30 phút nữa sẽ hết hạn.\n"
            "**Deadline:** 21:00 hôm nay\n"
            "**Nguồn:** #announcements · Lab Coach"
        )

    except discord.Forbidden:
        pass


if not settings.discord_bot_token:
    raise RuntimeError(
        "Thiếu DISCORD_BOT_TOKEN trong .env"
    )


bot.run(
    settings.discord_bot_token
)