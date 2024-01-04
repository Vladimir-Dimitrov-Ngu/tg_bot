from typing import Iterable
import config
import aiosqlite
import logging 


async def _insert_user(telegram_user_id: int) -> None:
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        await db.execute(
            f"INSERT OR IGNORE INTO bot_user (telegram_id) VALUES ({telegram_user_id})"
        )
        await db.commit()
