import discord

PRIORITY_ICON = {
    "high": "🔴",
    "medium": "🟠",
    "low": "🟢",
}

def build_summary_embed(items: list[dict], task_ids: list[int], channel_names: list[str], scanned_count: int) -> discord.Embed:
    embed = discord.Embed(
        title="📌 AI Discord Summary",
        description=(
            f"Đã quét **{len(channel_names)} channel** · **{scanned_count} message**\n"
            + "Phạm vi: " + ", ".join(f"`#{x}`" for x in channel_names)
        ),
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
            parts.append(f"Confidence: `{conf:.2f}`")
        except Exception:
            pass

        embed.add_field(
            name=f"{icon} {item_type} · {title}",
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
