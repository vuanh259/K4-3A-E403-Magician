import json
from datetime import datetime
from pathlib import Path
from typing import Any

import aiosqlite

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    guild_id TEXT,
    channel_name TEXT,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    priority TEXT NOT NULL,
    deadline_iso TEXT,
    confidence REAL,
    source_message_id TEXT,
    source_url TEXT,
    source_author TEXT,
    source_message TEXT,
    reason TEXT,
    status TEXT NOT NULL DEFAULT 'open',
    reminder_sent INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS summary_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    guild_id TEXT,
    channels_json TEXT NOT NULL,
    message_count INTEGER NOT NULL,
    item_count INTEGER NOT NULL,
    created_at TEXT NOT NULL
);
"""

class Store:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def init(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            await db.executescript(SCHEMA)
            await db.commit()

    async def save_summary_run(self, user_id: int, guild_id: int | None, channels: list[str], message_count: int, item_count: int):
        now = datetime.utcnow().isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO summary_runs(user_id,guild_id,channels_json,message_count,item_count,created_at) VALUES(?,?,?,?,?,?)",
                (str(user_id), str(guild_id) if guild_id else None, json.dumps(channels, ensure_ascii=False), message_count, item_count, now),
            )
            await db.commit()

    async def upsert_items(self, user_id: int, guild_id: int | None, items: list[dict[str, Any]]) -> list[int]:
        ids: list[int] = []
        now = datetime.utcnow().isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            for item in items:
                cur = await db.execute(
                    """
                    INSERT INTO tasks(
                        user_id,guild_id,channel_name,title,type,priority,deadline_iso,confidence,
                        source_message_id,source_url,source_author,source_message,reason,status,
                        reminder_sent,created_at,updated_at
                    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,'open',0,?,?)
                    """,
                    (
                        str(user_id),
                        str(guild_id) if guild_id else None,
                        item.get("source_channel"),
                        item.get("title") or "Untitled",
                        item.get("type") or "info",
                        item.get("priority") or "medium",
                        item.get("deadline_iso"),
                        float(item.get("confidence") or 0),
                        item.get("source_message_id"),
                        item.get("source_url"),
                        item.get("source_author"),
                        item.get("source_message"),
                        item.get("reason"),
                        now,
                        now,
                    ),
                )
                ids.append(cur.lastrowid)
            await db.commit()
        return ids

    async def list_open_tasks(self, user_id: int, limit: int = 20) -> list[dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute(
                "SELECT * FROM tasks WHERE user_id=? AND status='open' ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, deadline_iso IS NULL, deadline_iso LIMIT ?",
                (str(user_id), limit),
            )
            rows = await cur.fetchall()
            return [dict(r) for r in rows]

    async def get_task(self, task_id: int, user_id: int | None = None) -> dict | None:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            if user_id is None:
                cur = await db.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
            else:
                cur = await db.execute("SELECT * FROM tasks WHERE id=? AND user_id=?", (task_id, str(user_id)))
            row = await cur.fetchone()
            return dict(row) if row else None

    async def mark_done(self, task_id: int, user_id: int) -> bool:
        now = datetime.utcnow().isoformat()
        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(
                "UPDATE tasks SET status='done', updated_at=? WHERE id=? AND user_id=?",
                (now, task_id, str(user_id)),
            )
            await db.commit()
            return cur.rowcount > 0

    async def correct_task(self, task_id: int, user_id: int, deadline_iso: str | None = None, priority: str | None = None, title: str | None = None) -> bool:
        fields = []
        values = []
        if deadline_iso is not None:
            fields.append("deadline_iso=?")
            values.append(deadline_iso or None)
        if priority is not None:
            fields.append("priority=?")
            values.append(priority)
        if title is not None:
            fields.append("title=?")
            values.append(title)
        if not fields:
            return False

        fields += ["reminder_sent=0", "updated_at=?"]
        values.append(datetime.utcnow().isoformat())
        values += [task_id, str(user_id)]

        async with aiosqlite.connect(self.db_path) as db:
            cur = await db.execute(
                f"UPDATE tasks SET {', '.join(fields)} WHERE id=? AND user_id=?",
                tuple(values),
            )
            await db.commit()
            return cur.rowcount > 0

    async def due_reminders(self, now_iso: str, reminder_cutoff_iso: str) -> list[dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute(
                """
                SELECT * FROM tasks
                WHERE status='open'
                  AND reminder_sent=0
                  AND deadline_iso IS NOT NULL
                  AND deadline_iso > ?
                  AND deadline_iso <= ?
                ORDER BY deadline_iso
                """,
                (now_iso, reminder_cutoff_iso),
            )
            rows = await cur.fetchall()
            return [dict(r) for r in rows]

    async def mark_reminder_sent(self, task_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE tasks SET reminder_sent=1 WHERE id=?", (task_id,))
            await db.commit()
