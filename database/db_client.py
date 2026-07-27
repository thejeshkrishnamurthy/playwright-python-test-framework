import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

DATABASE_PATH = Path("database/test_data.db")

BookingRecord = tuple[int, str, str, int, str]


@contextmanager
def database_connection() -> Generator[sqlite3.Connection]:
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        yield connection
    finally:
        connection.close()


def insert_booking(
    booking_id: int,
    first_name: str,
    last_name: str,
    total_price: int,
    status: str,
) -> None:
    with database_connection() as connection:
        connection.execute(
            """
            INSERT OR REPLACE INTO bookings (
                booking_id,
                first_name,
                last_name,
                total_price,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                booking_id,
                first_name,
                last_name,
                total_price,
                status,
            ),
        )
        connection.commit()


def get_booking(
    booking_id: int,
) -> BookingRecord | None:
    with database_connection() as connection:
        cursor = connection.execute(
            """
            SELECT
                booking_id,
                first_name,
                last_name,
                total_price,
                status
            FROM bookings
            WHERE booking_id = ?
            """,
            (booking_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return (
            int(row[0]),
            str(row[1]),
            str(row[2]),
            int(row[3]),
            str(row[4]),
        )
