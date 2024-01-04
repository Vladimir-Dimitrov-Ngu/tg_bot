import aiosqlite
from typing import Iterable
import config
from user import _insert_user
import logging

logger = logging.getLogger(__name__)

async def actual_voting_id() -> int | None:
    sql = """SELECT id 
    FROM voting 
    WHERE voting_start <= current_date
        AND voting_finish >= current_date
    ORDER BY voting_start 
    LIMIT 1
    """
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(sql) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None
            return row["id"]
        
async def save_vote(telegram_user_id: int, book: Iterable) -> None:
    await _insert_user(telegram_user_id)
    vote_id = await actual_voting_id()
    if vote_id is None:
        logger.warning('No actual voting in save_vote()')
        return 
    sql = f"""INSERT OR REPLACE INTO vote 
        (vote_id, user_id, first_book, second_book, third_book) 
    VALUES ({vote_id}, {telegram_user_id}, {book[0].id}, {book[1].id}, {book[2].id})
    """
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        await db.execute(sql)
        await db.commit()
