import discord

PRIORITY_ICON = {
    "high": "🔴",
    "medium": "🟠",
    "low": "🟢",
}

def build_summary_embed(
    items: list[dict],
    task_ids: list[int],
    channel_names: list[str],
    scanned_count: int,
    is_new_flags: list[bool] | None = None,
    has_previous_run: bool = False,
) -> discord.Embed:
    is_new_flags = is_new_flags or [False] * len(items)
    new_count = sum(1 for f in is_new_flags if f)

    desc_lines = [
        f"Đã quét **{len(channel_names)} channel** · **{scanned_count} message**",
        "Phạm vi: " + ", ".join(f"`#{x}`" for x in channel_names),
    ]

    if has_previous_run:
        if new_count > 0:
            desc_lines.append(f"✨ **Phát hiện {new_count} thông báo MỚI** kể từ lần quét trước!")
        else:
            desc_lines.append("📋 **Toàn bộ thông báo trong 24h qua** *(không có tin mới thêm)*")

    embed = discord.Embed(
        title="📌 AI Discord Summary",
        description="\n".join(desc_lines),
        color=discord.Color.blurple(),
        timestamp=discord.utils.utcnow(),
    )

    if not items:
        embed.add_field(
            name="Không có việc quan trọng rõ ràng",
            value="AI không tìm thấy task/deadline/thay đổi lịch có đủ căn cứ.",
            inline=False,
        )
        return embed

    for idx, item in enumerate(items[:10]):
        task_id = task_ids[idx] if idx < len(task_ids) else None
        priority = str(item.get("priority", "medium")).lower()
        icon = PRIORITY_ICON.get(priority, "🟡")
        item_type = str(item.get("type", "info")).upper()
        title = str(item.get("title", "Thông tin cần chú ý"))[:180]

        is_item_new = is_new_flags[idx] if idx < len(is_new_flags) else False
        new_tag = "🆕 " if (has_previous_run and is_item_new) else ""

        parts = []
        if task_id:
            parts.append(f"**Task ID:** `{task_id}`")

        if item.get("deadline_iso"):
            parts.append(f"**Deadline:** `{item['deadline_iso']}`")

        if item.get("reason"):
            parts.append(str(item["reason"])[:320])

        src = " · ".join(x for x in [f"#{item.get('source_channel')}" if item.get("source_channel") else "", item.get("source_author") or ""] if x)
        if src:
            if item.get("source_url"):
                parts.append(f"**Nguồn:** [{src}]({item['source_url']})")
            else:
                parts.append(f"**Nguồn:** {src}")

        snippet = (item.get("source_message") or "").replace("\n", " ")[:200]
        if snippet:
            parts.append(f"> {snippet}")

        try:
            conf = float(item.get("confidence", 0))
            if conf < 0.8:
                parts.append(f"Confidence: `{conf:.2f}` ⚠️ *(Mốc giờ/thông tin cần xác nhận lại)*")
            else:
                parts.append(f"Confidence: `{conf:.2f}`")
        except Exception:
            pass

        embed.add_field(
            name=f"{icon} {new_tag}{item_type} · {title}",
            value="\n".join(parts)[:1024],
            inline=False,
        )

    embed.set_footer(
        text="AI chỉ hỗ trợ lọc. User vẫn kiểm tra message nguồn và có thể /correct hoặc /done."
    )
    return embed

def build_tasks_embed(tasks: list[dict]) -> discord.Embed:
    embed = discord.Embed(
        title="🗂️ Việc đang theo dõi",
        color=discord.Color.blurple(),
    )
    if not tasks:
        embed.description = "Bạn chưa có task đang mở."
        return embed

    for task in tasks[:20]:
        icon = PRIORITY_ICON.get(task["priority"], "🟡")
        deadline = task["deadline_iso"] or "Chưa có"
        embed.add_field(
            name=f"{icon} #{task['id']} · {task['title']}",
            value=(
                f"Loại: `{task['type']}`\n"
                f"Deadline: `{deadline}`\n"
                f"Nguồn: `#{task['channel_name'] or 'unknown'}`"
            ),
            inline=False,
        )
    return embed
