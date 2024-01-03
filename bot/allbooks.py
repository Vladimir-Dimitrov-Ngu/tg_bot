import aiosqlite
from dataclasses import dataclass
from datetime import datetime
from typing import List

import config


@dataclass
class Book:
    id: int
    name: str
    category_id: int
    category_name: str
    read_start: datetime
    read_finish: datetime


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
                id=book.category_id,
                name=book.category_name,
                books=[book]
            )
            categories.append(category)
            category_id = book.category_id
            continue
        categories[-1].books.append(book)
    return categories

async def get_all_books() -> list[Category]:
    books = []
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
        SELECT
            b.id as book_id,
            b.name as book_name, 
            c.id as category_id,
            c.name as category_name,
            b.read_start, b.read_finish
        FROM book as b
        LEFT JOIN book_category c ON c.id=b.category_id 
        ORDER BY c."ordering", b."ordering"
        """
        ) as cursor:
            async for row in cursor:
                books.append(
                    Book(
                        id=row["book_id"],
                        name=row["book_name"],
                        category_name=row["category_name"],
                        category_id = row['category_id'],
                        read_start=row["read_start"],
                        read_finish=row["read_finish"],
                    )
                )
    return _group_books_by_category(books)
