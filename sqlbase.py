import sqlite3
import hashlib

class SQLBase():
    def __init__(self):
        self.con = sqlite3.connect('users.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.createBase()
    
    def __del__(self):
        self.con.commit()
    
    def createBase(self):
        self.cur.execute('DROP TABLE users')
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    userID INT IDENTITY(1,1) PRIMARY KEY,
	                login NVARCHAR(15) NOT NULL UNIQUE,
                    password varchar(250) NOT NULL
                )
                """)
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS passwords
                (
                    userID INT PRIMARY KEY,
                    hash BINARY(64) NOT NULL,
                    salt UNIQUEIDENTIFIER NOT NULL,
                    FOREIGN KEY(userID) REFERENCES users(userID)
                )
                """)
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS relationshipStatus
                (
                    statusID INT IDENTITY(1,1) PRIMARY KEY,
                    statusDescription NVARCHAR(20) NOT NULL
                )
                """)
        self.cur.execute(
            """
                CREATE TABLE IF NOT EXISTS relationships
                (
                    firstUserID INT NOT NULL,
                    secondUserID INT NOT NULL,
                    statusID INT NOT NULL,
                    PRIMARY KEY(firstUserID, secondUserID),
                    FOREIGN KEY(firstUserID) REFERENCES users(userID),
                    FOREIGN KEY(secondUserID) REFERENCES users(userID),
                    FOREIGN KEY(statusID) REFERENCES relationshipStatus(statusID)
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