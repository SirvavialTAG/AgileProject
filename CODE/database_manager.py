import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="vocabulary.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    front TEXT NOT NULL,
                    back TEXT NOT NULL,
                    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    next_review_date DATE NOT NULL,
                    last_interval_days INTEGER DEFAULT 0
                )
            ''')

    def add_card(self, front, back):
        next_review_date = datetime.now().date()
        with self.connection:
            self.connection.execute(
                "INSERT INTO cards (front, back, next_review_date) VALUES (?, ?, ?)",
                (front, back, next_review_date)
            )

    def get_cards(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM cards").fetchall()

    def delete_card(self, card_id):
        with self.connection:
            self.connection.execute("DELETE FROM cards WHERE id = ?", (card_id,))

    def update_card_review_date(self, card_id, next_review_date, last_interval_days):
        with self.connection:
            self.connection.execute(
                "UPDATE cards SET next_review_date = ?, last_interval_days = ? WHERE id = ?",
                (next_review_date, last_interval_days, card_id)
            )

    def close(self):
        self.connection.close()