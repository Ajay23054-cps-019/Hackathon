from fastapi import FastAPI
import hashlib
import sqlite3
import uuid

app = FastAPI()

#class for database
class Database:

    def __init__(self):
        self.conn = sqlite3.connect("databases/database.db")
        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            uuid TEXT PRIMARY KEY,
            uid INTEGER UNIQUE,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            created_time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    def check_login(self, uuid: str, email: str, password: str):

        db_pass = self.get_pass(uuid, email)

        if db_pass is None:
            return False

        if self.verify_password(password, db_pass):
            return True

        return False

    def get_pass(self, uuid: str, email: str):

        self.cur.execute(
            "SELECT password FROM users WHERE email = ? AND uuid = ?",
            (email, uuid)
        )


        passw = self.cur.fetchone()

        if passw:
            return passw[0]

        return None

    def verify_password(self, user_password: str, db_password: str):

        return self.hashed_password(user_password) == db_password

    def register(
        self,
        uuid: str,
        uid: int,
        name: str,
        email: str,
        password: str
    ):

        password = self.hashed_password(password)

        self.cur.execute("""
            INSERT INTO users (uuid, uid, name, email, password)
            VALUES (?, ?, ?, ?, ?)
        """, (uuid, uid, name, email, password))

        self.conn.commit()

    def hashed_password(self, password: str):

        return hashlib.sha256(
            password.encode()
        ).hexdigest()

    def generate_uuid(self):

        return str(uuid.uuid4())
    



#API starts from here
@app.get("/login")
def login(uuid : int,email : str,password : str):
    return "login"


@app.get("/register")
def register(name : str,email : str,password : str):
    return "register"

@app.get("logout")
def logout(uuid : int):
    return "logged out"

