import sqlite3

import bcrypt

from src.models import SensorData, User


class Database:
    def __init__(self, name: str) -> None:
        self.conn = sqlite3.connect(name)
        self.init_db()

    def init_db(self) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL,
                humidity REAL,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def insert_data(self, data: "SensorData") -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO sensor_data (temperature, humidity, status)
            VALUES (?, ?, ?)
            """,
            (data.temperature, data.humidity, data.status),
        )
        self.conn.commit()

    def get_data(self, start: str | None = None, end: str | None = None) -> list[SensorData]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT temperature, humidity, status, timestamp FROM sensor_data
            WHERE (timestamp >= ? OR ? IS NULL) AND (timestamp <= ? OR ? IS NULL)
            ORDER BY timestamp DESC
            """,
            (start, start, end, end),
        )
        rows = cursor.fetchall()
        return [
            SensorData(temperature=row[0], humidity=row[1], status=row[2], timestamp=row[3])
            for row in rows
        ]


    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            bytes(plain_password, encoding="utf-8"),
            bytes(hashed_password, encoding="utf-8"),
        )

    def verify_user(self, username: str, password: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT password FROM users WHERE username = ?
            """,
            (username,),
        )
        row = cursor.fetchone()
        if row is None:
            return False
        stored_password = row[0]
        return self.verify_password(password, stored_password)

    def get_password_hash(self, password: str) -> str:
        return bcrypt.hashpw(
            bytes(password, encoding="utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    def get_users(self) -> list[User]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, username FROM users
            """
        )
        rows = cursor.fetchall()
        return [User(id=row[0], username=row[1]) for row in rows]

    def create_user(self, username: str, password: str) -> User:
        password = self.get_password_hash(password)
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
            """
        )
        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, password),
        )
        self.conn.commit()
        return User(id=cursor.lastrowid, username=username)
