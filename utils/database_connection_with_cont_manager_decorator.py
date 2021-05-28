from contextlib import contextmanager
import sqlite3


@contextmanager
def database_connection(host: str):
    connection = sqlite3.connect(host)
    cursor = connection.cursor()
    try:
        yield cursor

    finally:
        connection.commit()
        connection.close()


@contextmanager
def error_handler():
    try:
        yield
    except sqlite3.IntegrityError:
        print(f"This book cannot be added to your collection. A book with the same name already exists in your "
              f"collection.")
