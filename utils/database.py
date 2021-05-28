import sqlite3
from typing import List, Dict, Union

from .database_connection import DatabaseConnection
from .database_connection_with_cont_manager_decorator import database_connection, error_handler

SQLITE_FILE_NAME = "data.db"
MISSING_BOOK_MESSAGE = "\"{name}\" is not found in your book collection."
Book = Dict[str, Union[str, int]]  # type of expected book dictionary parameter where all keys must be strings and values can be strings or integers


def _connect_to_db(db_command: str, *args: str) -> None:
    with database_connection(SQLITE_FILE_NAME) as cursor:
        cursor.execute(db_command, (*args,))


def get_book_collection() -> List[Book]:
    with database_connection(SQLITE_FILE_NAME) as cursor:
        cursor.execute("SELECT * FROM books")
        # fetchall() returns list of tuples [(name, author, read), (name, author, read)] - we transform it into dictionary
        books = [{"name": row[0], "author": row[1], "read": row[2]} for row in cursor.fetchall()]
    return books


def _check_if_book_in_collection(query_book_name: str) -> bool:
    return len([book for book in get_book_collection() if book["name"] == query_book_name]) > 0


def create_db_table() -> None:
    _connect_to_db("CREATE TABLE IF NOT EXISTS books (name text primary key, author text, read integer)")


@error_handler()
def add_book(name: str, author: str) -> None:
    _connect_to_db("INSERT INTO books VALUES(?, ?, 0)", name, author)
    print(f"\"{name}\" by {author} was added to your book collection successfully!")


def mark_book_as_read(name: str) -> None:
    if _check_if_book_in_collection(name):
        _connect_to_db("UPDATE books SET read = 1 WHERE name = ?", name)
        print(f"\"{name}\" was marked as \"Read\" successfully!")
    else:
        print(MISSING_BOOK_MESSAGE.format(name=name))


def delete_book(name: str) -> None:
    if _check_if_book_in_collection(name):
        _connect_to_db("DELETE FROM books WHERE name = ?", name)
        print(f"\"{name}\" was removed from your book collection successfully!")
    else:
        print(MISSING_BOOK_MESSAGE.format(name=name))
