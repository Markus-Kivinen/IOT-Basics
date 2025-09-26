import sqlite3

from passlib.context import CryptContext

from src.models import SensorData


class Database:
    def __init__(self, name: str) -> None:
        self.conn = sqlite3.connect(name)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
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

    def get_data(self) -> list[SensorData]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT temperature, humidity, status FROM sensor_data
            ORDER BY timestamp DESC
            """
        )
        rows = cursor.fetchall()
        return [
            SensorData(temperature=row[0], humidity=row[1], status=row[2])
            for row in rows
        ]

    def verify_user(
        self, username: str, password: str
    ) -> bool:
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
        return self.pwd_context.verify(password, stored_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_user(self, username: str, password: str) -> None:
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
