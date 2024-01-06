import aiosqlite
import logging
from datetime import datetime
from typing import Iterable
from dataclasses import dataclass


import config
from user import _insert_user


@dataclass
class BookVoteResult:
    book_name: str
    score: int


@dataclass
class VoteResult:
    vote_start: str
    vote_finish: str
    leaders: list


@dataclass
class Voting:
    id: int
    vote_start: str
    vote_finish: str

    def __post_init__(self):
        """Format read_start and read_finish to needed string format"""
        for fieid in ("vote_start", "vote_finish"):
            value = getattr(self, fieid)
            if value is None:
                continue
            value = datetime.strptime(value, "%Y-%m-%d").strftime(config.DATE_FORMAT)
            setattr(self, fieid, value)


logger = logging.getLogger(__name__)


async def get_actual_voting() -> Voting | None:
    sql = """SELECT id, voting_start, voting_finish
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
            return Voting(
                id=row["id"],
                vote_start=row["voting_start"],
                vote_finish=row["voting_finish"],
            )


async def save_vote(telegram_user_id: int, book: Iterable) -> None:
    await _insert_user(telegram_user_id)
    vote_id = await get_actual_voting()
    if vote_id is None:
        logger.warning("No actual voting in save_vote()")
        return
    sql = f"""INSERT OR REPLACE INTO vote
        (vote_id, user_id, first_book, second_book, third_book)
    VALUES ({vote_id.id}, {telegram_user_id}, {book[0].id}, {book[1].id}, {book[2].id})
    """
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        await db.execute(sql)
        await db.commit()


async def get_leaders() -> VoteResult | None:
    actual_voting = await get_actual_voting()
    vote_results = VoteResult(
        vote_start=actual_voting.vote_start,
        vote_finish=actual_voting.vote_finish,
        leaders=[],
    )
    sql = f"""
        SELECT t2.*, b.name AS book_name FROM
            (SELECT t.book_id, SUM(t.score) as total_score FROM (
                SELECT first_book AS book_id, 3 * COUNT(*) as score
                FROM vote v WHERE vote_id = {actual_voting.id} GROUP BY first_book

                UNION

                SELECT second_book  AS book_id, 2 * COUNT(*) as score
                FROM vote v WHERE vote_id = {actual_voting.id} GROUP BY second_book

                UNION

                SELECT third_book  AS book_id, 1 * COUNT(*) as score
                FROM vote v WHERE vote_id = {actual_voting.id} GROUP BY third_book
            ) t
            GROUP BY book_id
            ORDER BY total_score DESC
            LIMIT 5) t2
        LEFT JOIN book b ON b.id=t2.book_id
        """
    actual_voting = get_actual_voting()
    if actual_voting is None:
        return None
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(sql) as cursor:
            async for row in cursor:
                vote_results.leaders.append(
                    BookVoteResult(book_name=row["book_name"], score=row["total_score"])
                )
    return vote_results
