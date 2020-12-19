import sqlite3
import hashlib

class SQLBase():
    def __init__(self):
        self.con = sqlite3.connect('users.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
    
    def __del__(self):
        self.con.commit()
    
    def createBase(self):
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY ASC,
                    login varchar(250) NOT NULL UNIQUE,
                    password varchar(250) NOT NULL
                )
                """)

    def getUser(self, login, password):
        values = login, hashlib.sha3_256(password.encode()).hexdigest()
        self.cur.execute('SELECT id FROM users WHERE login=? AND password=?', values)
        id = self.cur.fetchone()
        if not id:
            return None

        return id[0]
    
    def addUser(self, login, password):
        try:
            values = login, hashlib.sha3_256(password.encode()).hexdigest()
            self.cur.execute('INSERT INTO users(login, password) VALUES(?, ?)', values)
            return True
        except sqlite3.IntegrityError:
            return False
    
    def removeUser(self, login, password):
        values = login, password
        self.cur.execute('DELETE FROM users WHERE login=? AND password=?', values)