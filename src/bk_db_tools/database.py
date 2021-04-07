import sqlite3
from pathlib import Path
from settings import Settings

class Database:
    """
    pulled from
    https://stackoverflow.com/questions/38076220/python-mysqldb-connection-in-a-class
    and adapted from there.
    
    This will let you use the Database class either normally like db = Database('db_file.sqlite) or in a with statement:

        with Database('db_file.sqlite') as db:
            # do stuff
            
    and the connection will automatically commit and close when the with statement exits.

    Then, you can encapsulate specific queries that you do often in methods and make them easy to access. For example, if you're dealing with transaction records, you could have a method to get them by date:

        def transactions_by_date(self, date):
            sql = "SELECT * FROM transactions WHERE transaction_date = ?"
            return self.query(sql, (date,))
    
    Here's some sample code where we create a table, add some data, and then read it back out:

        with Database('my_db.sqlite') as db:
            db.execute('CREATE TABLE comments(pkey INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR, comment_body VARCHAR, date_posted TIMESTAMP)')
            db.execute('INSERT INTO comments (username, comment_body, date_posted) VALUES (?, ?, current_date)', ('tom', 'this is a comment'))
            comments = db.query('SELECT * FROM comments')
            print(comments)
    """
    
    def __init__(self):
        dbPath = Path(Settings.databasePath)
        
        self._conn = sqlite3.connect(dbPath)
        self._conn.row_factory = sqlite3.Row
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        
    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()