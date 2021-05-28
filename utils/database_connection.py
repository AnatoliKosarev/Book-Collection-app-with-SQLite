import sqlite3


class DatabaseConnection:

    def __init__(self, host: str):
        self.host = host
        self.connection = None
        self.cursor = None

    # is called when you go in context manager before you start running it
    def __enter__(self) -> sqlite3.Cursor:
        self.connection = sqlite3.connect(self.host)
        self.cursor = self.connection.cursor()
        return self.cursor

    # is called when you leave context manager
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb: # closes the connection to db without commiting when sqlite exception was raised to prevent leaving db in inconsistent state
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
