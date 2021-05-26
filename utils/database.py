import sqlite3

SQLITE_FILE_NAME = "data.db"
MISSING_BOOK_MESSAGE = "\"{name}\" is not found in your book collection."


def _connect_to_db(db_command, *args):
    connection = sqlite3.connect(SQLITE_FILE_NAME)
    cursor = connection.cursor()
    cursor.execute(db_command, (*args,))
    connection.commit()
    connection.close()


def get_book_collection():
    connection = sqlite3.connect(SQLITE_FILE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    # fetchall() returns list of tuples [(name, author, read), (name, author, read)] - we transform it into dictionary
    books = [{"name": row[0], "author": row[1], "read": row[2]} for row in cursor.fetchall()]
    connection.close()
    return books


def _check_if_book_in_collection(query_book_name):
    return len([book for book in get_book_collection() if book["name"] == query_book_name]) > 0


def create_db_table():
    _connect_to_db("CREATE TABLE IF NOT EXISTS books (name text primary key, author text, read integer)")


def add_book(name, author):
    try:
        _connect_to_db("INSERT INTO books VALUES(?, ?, 0)", name, author)
        print(f"\"{name}\" by {author} was added to your book collection successfully!")
    except sqlite3.IntegrityError:
        print(f"\"{name}\" cannot be added to your collection. Book with the same name already exists in your "
              f"collection.")


def mark_book_as_read(name):
    if _check_if_book_in_collection(name):
        _connect_to_db("UPDATE books SET read = 1 WHERE name = ?", name)
        print(f"\"{name}\" was marked as \"Read\" successfully!")
    else:
        print(MISSING_BOOK_MESSAGE.format(name=name))


def delete_book(name):
    if _check_if_book_in_collection(name):
        _connect_to_db("DELETE FROM books WHERE name = ?", name)
        print(f"\"{name}\" was removed from your book collection successfully!")
    else:
        print(MISSING_BOOK_MESSAGE.format(name=name))
