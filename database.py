import sqlite3

class TestDB:
    def __init__(self):
        self.database = 'mm_test.db'
        self.connection = self.openConnect()

    def openConnect(self):
        print("Opened database successfully")
        return sqlite3.connect(self.database)

    def setup(self):
        self.connection.execute('''CREATE TABLE IF NOT EXISTS user_tags
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         USER_UUID      CHAR(255)   NOT NULL,
         TAG            CHAR(255)   NOT NULL);''')
        print("Table if not existed created successfully")
        self.connection.close()

    def drop_user_tags(self):
        self.connection.execute('''DROP TABLE user_tags''')

    def last_row(self):
        return self.connection.execute('''SELECT * FROM user_tags''')
