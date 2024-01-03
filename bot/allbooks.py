import aiosqlite
from dataclasses import dataclass
from datetime import datetime
from typing import List

import config


def _chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


@dataclass
class Book:
    id: int
    name: str
    category_name: str
    read_start: datetime
    read_finish: datetime


@dataclass
class Category:
    id: int
    name: str
    books: List[int]


async def get_all_books(chunk_size: int = 50) -> list[Category]:
    books = []
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            """
select
b.id as book_id,
b.name as book_name, 
c.id as category_id,
c.name as category_name,
b.read_start, b.read_finish
from book as b
left join book_category c on c.id=b.category_id 
order by c."ordering", b."ordering"
"""
        ) as cursor:
            async for row in cursor:
                books.append(
                    Book(
                        id=row["book_id"],
                        name=row["book_name"],
                        category_name=row["category_name"],
                        read_start=row["read_start"],
                        read_finish=row["read_finish"],
                    )
                )
    return _chunks(books, chunk_size)
