import aiosqlite
from dataclasses import dataclass
from datetime import datetime
from typing import LiteralString
from typing import List

import config


@dataclass
class Book:
    id: int
    name: str
    category_id: int
    category_name: str
    read_start: str
    read_finish: str

    def __post_init__(self):
        """Format read_start and read_finish to needed string format"""
        for fieid in ("read_start", "read_finish"):
            value = getattr(self, fieid)
            if value is None:
                continue
            value = datetime.strptime(value, "%Y-%m-%d").strftime(config.DATE_FORMAT)
            setattr(self, fieid, value)


@dataclass
class Category:
    id: int
    name: str
    books: List[int]


def _group_books_by_category(books: list[Book]) -> list[Category]:
    categories = []
    category_id = None
    for book in books:
        if category_id != book.category_id:
            category = Category(
                id=book.category_id, name=book.category_name, books=[book]
            )
            categories.append(category)
            category_id = book.category_id
            continue
        categories[-1].books.append(book)
    return categories


async def get_all_books() -> list[Category]:
    books = []
    sql = (
        _get_books_base_sql()
        + """
        ORDER BY c."ordering", b."ordering" """
    )
    books = await _get_books_from_db(sql)
    return _group_books_by_category(books)


async def get_allready_all_books() -> list[Book]:
    sql = (
        _get_books_base_sql() + """
        WHERE read_start < current_date 
        AND read_finish <= current_date
        ORDER BY b.read_start
        """
    )
    return await _get_books_from_db(sql)

async def get_non_started_books() -> list[Book]:
    sql  = (
        _get_books_base_sql() + """
        WHERE b.read_start IS NULL
        ORDER BY c."ordering", b."ordering"
        """
    )
    books = await _get_books_from_db(sql)
    return _group_books_by_category(books)
    


async def get_now_books() -> list[Book]:
    sql = (
        _get_books_base_sql()
        + """
        WHERE read_start < current_date 
        AND read_finish >= current_date
        ORDER BY b.read_start
        """
    )
    return await _get_books_from_db(sql)


def _get_books_base_sql() -> LiteralString:
    return """
        SELECT
            b.id as book_id,
            b.name as book_name, 
            c.id as category_id,
            c.name as category_name,
            b.read_start, b.read_finish
        FROM book as b
        LEFT JOIN book_category c ON c.id=b.category_id 
    """


async def _get_books_from_db(sql: LiteralString) -> list[Book]:
    books = []
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(sql) as cursor:
            async for row in cursor:
                books.append(
                    Book(
                        id=row["book_id"],
                        name=row["book_name"],
                        category_name=row["category_name"],
                        category_id=row["category_id"],
                        read_start=row["read_start"],
                        read_finish=row["read_finish"],
                    )
                )
    return books
