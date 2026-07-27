import sqlite3
from pathlib import Path

DATABASE_PATH = Path("database/test_data.db")


def initialise_database() -> None:
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                total_price INTEGER NOT NULL,
                status TEXT NOT NULL
            )
            """)

        connection.commit()


if __name__ == "__main__":
    initialise_database()
