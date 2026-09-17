import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import discord

from config import settings
from storage import Store

class ReminderService:
    def __init__(self, bot: discord.Client, store: Store):
        self.bot = bot
        self.store = store
        self.task: asyncio.Task | None = None

    def start(self):
        if self.task is None or self.task.done():
            self.task = asyncio.create_task(self._loop())

    async def _loop(self):
        tz = ZoneInfo(settings.timezone)
        while not self.bot.is_closed():
            try:
                now = datetime.now(tz)
                cutoff = now + timedelta(minutes=settings.reminder_minutes_before)
                due = await self.store.due_reminders(
                    now_iso=now.isoformat(),
                    reminder_cutoff_iso=cutoff.isoformat(),
                )

                for task in due:
                    user = self.bot.get_user(int(task["user_id"]))
                    if user is None:
                        try:
                            user = await self.bot.fetch_user(int(task["user_id"]))
                        except discord.HTTPException:
                            user = None

                    if user:
                        text = (
                            "⏰ **DEADLINE REMINDER**\n"
                            f"**{task['title']}** sắp đến hạn.\n"
                            f"Deadline: **{task['deadline_iso']}**\n"
                            f"Nguồn: **#{task['channel_name'] or 'unknown'} · {task['source_author'] or 'unknown'}**\n"
                        )
                        if task.get("source_url"):
                            text += f"Message gốc: {task['source_url']}\n"

                        try:
                            await user.send(text)
                        except discord.Forbidden:
                            pass

                    await self.store.mark_reminder_sent(task["id"])
            except Exception as e:
                print("Reminder loop error:", repr(e))

            await asyncio.sleep(settings.reminder_poll_seconds)
