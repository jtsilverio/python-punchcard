import datetime
from typing import List

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


def clockin() -> None:
    current_date, current_time = now()
    today_punchcard = get_punchcard(current_date)

    if today_punchcard is None:
        punchcard = Punchcard(date=current_date)
        entry = Entry(start_time=current_time, punchcard=punchcard)
        punchcard.save()
        entry.save()
    else:
        last_entry = get_last_entry(today_punchcard)
        if last_entry is not None:
            if last_entry.end_time is None:
                raise NotClockedOutError()

        entry = Entry(start_time=current_time, punchcard=today_punchcard)
        entry.save()


def clockout() -> None:
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


# def list_entries(date: datetime.date) -> List:  # pylint: disable=redefined-outer-name
#     if not isinstance(date, (datetime.date, datetime.datetime)):
#         raise ValueError("date must be a datetime object")

#     return get_entries(date.strftime("%Y-%m-%d"))


if __name__ == "__main__":
    # print(list_entries(datetime.date.today()))
