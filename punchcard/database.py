import sqlite3
from datetime import date, datetime

from punchcard.constants import DATABASE_PATH
from punchcard.models import Punchcard

conn = sqlite3.connect(DATABASE_PATH)
c = conn.cursor()
create_tables()


def create_tables():
    c.execute("""
        CREATE TABLE IF NOT EXISTS punchcard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start TEXT NOT NULL,
            end TEXT
        )
    """)


def last_punchcard() -> Punchcard | None:
    with conn:
        c.execute(
            "SELECT start, end, id FROM punchcard ORDER BY id DESC LIMIT 1"
        )
        row = c.fetchone()

    if row is None:
        return None

    start = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") if row[0] else None
    end = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S") if row[1] else None
    sqliteid = row[2] if row[2] else None

    return Punchcard(
        start=start,
        end=end,
        sqliteid=sqliteid,
    )


def clockin(punchcard: Punchcard):
    last_punchcard = get_last_punchcard()
    if last_punchcard is not None:
        if last_punchcard.end is None:
            raise ValueError("There is still a open Punchcard")

    if punchcard.end is not None:
        raise ValueError("Punchcard has already been clocked out")

    with conn:
        c.execute(
            "INSERT INTO punchcard (start, end) VALUES (:start, :end)",
            {
                "start": punchcard.start.strftime("%Y-%m-%d %H:%M:%S"),
                "end": punchcard.end,
            },
        )
    punchcard.sqliteid = c.lastrowid


def clockout(punchcard: Punchcard):
    punchcard.clockout()
    with conn:
        c.execute(
            "UPDATE punchcard SET end = :end WHERE start = :start",
            {
                "start": punchcard.start.strftime("%Y-%m-%d %H:%M:%S"),
                "end": punchcard.end.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )


def get_punchcards(date: date = None):  # pylint: disable=redefined-outer-name
    if date is None:
        date = datetime.now().date()

    with conn:
        c.execute(
            "SELECT start, end FROM punchcard WHERE date(start) = date(:start)",
            {"start": date.strftime("%Y-%m-%d")},
        )
        rows = c.fetchall()
    return rows


if __name__ == "__main__":
    card = Punchcard(start=datetime.now())
    last = get_last_punchcard()
    clockout(last)
