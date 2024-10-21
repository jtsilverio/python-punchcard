from typing import List, Tuple

import peewee

from punchcard.config import DATABASE_PATH
from punchcard.exceptions import (
    AlreadyClockedOutError,
    NotClockedinError,
    NotClockedOutError,
)
from punchcard.models import Entry, Punchcard
from punchcard.time import now

db = peewee.SqliteDatabase(DATABASE_PATH)


def get_punchcard(date: str) -> Punchcard | None:
    return Punchcard.select().where(Punchcard.date == date).get_or_none()  # type: ignore


def get_entries(date: str) -> List[Entry]:
    punchcard = get_punchcard(date)
    if punchcard is None:
        return []
    return list(punchcard.entries)


def get_last_entry(punchcard: Punchcard) -> Entry | None:
    return punchcard.entries.select().order_by(Entry.id.desc()).get_or_none()  #  type: ignore


def clockin() -> Tuple[Punchcard, Entry]:
    current_date, current_time = now()
    today_punchcard = get_punchcard(current_date)

    if today_punchcard is None:
        punchcard = Punchcard(date=current_date)
        entry = Entry(start_time=current_time, punchcard=punchcard)
        punchcard.save()
        entry.save()

        return punchcard, entry
    else:
        last_entry = get_last_entry(today_punchcard)
        if (last_entry is not None) and (last_entry.end_time is None):
            raise NotClockedOutError()

        entry = Entry(start_time=current_time, punchcard=today_punchcard)
        entry.save()

        return today_punchcard, entry


def clockout() -> Tuple[Punchcard, Entry]:
    current_date, current_time = now()

    today_punchcard = get_punchcard(current_date)
    if today_punchcard is None:
        raise NotClockedinError()

    last_entry = get_last_entry(today_punchcard)
    if last_entry is None:
        raise NotClockedinError()

    if last_entry.end_time is not None:
        raise AlreadyClockedOutError()

    last_entry.end_time = current_time
    last_entry.save()

    return today_punchcard, last_entry


if __name__ == "__main__":
    print(clockin())
