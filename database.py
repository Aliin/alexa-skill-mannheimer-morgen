import sqlite3

class TestDB:
    def __init__(self):
        self.database = 'mm_test.db'
        self.connection = connect(self)

    def connect(self):
        print("Opened database successfully")
        return sqlite3.connect(self.database)

    def setup(self):
        self.connection.execute('''CREATE TABLE IF NOT EXISTS user_tags
         (ID INT PRIMARY KEY        NOT NULL,
         USER_UUID      CHAR(255)   NOT NULL,
         TAG            CHAR(255)   NOT NULL);''')
        print("Table created successfully")
        self.connection.close()

