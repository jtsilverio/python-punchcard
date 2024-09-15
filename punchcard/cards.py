import datetime
from typing import List, Tuple

import peewee

from punchcard.config import get_user_config
from punchcard.constants import DATABASE_PATH
from punchcard.exceptions import AlreadyClockedOutError, NotClockedOutError
from punchcard.models import Punchcard

db = peewee.SqliteDatabase(DATABASE_PATH)
db.create_tables([Punchcard])


def now() -> Tuple[str, str]:
    datetime_now = datetime.datetime.now()
    date = datetime_now.date().strftime("%Y-%m-%d")
    time = datetime_now.time().strftime("%H:%M")
    return date, time


def get_last_punchcard() -> Punchcard | None:
    return Punchcard.select().order_by(Punchcard.id.desc()).get_or_none()  #  type: ignore


def clockin(punchcard: Punchcard) -> None:
    last_punchcard = get_last_punchcard()
    current_date, _ = now()
    if (
        (last_punchcard is not None)
        and (last_punchcard.date == current_date)
        and (last_punchcard.end is None)
    ):
        raise NotClockedOutError()

    if punchcard.end is not None:
        raise AlreadyClockedOutError()

    punchcard.save()


def clockout(punchcard: Punchcard) -> None:
    if punchcard.end is not None:
        raise AlreadyClockedOutError()

    _, end = now()
    punchcard.end = end
    punchcard.save()


def get_punchcards(date: datetime.date) -> List[Punchcard]:  # pylint: disable=redefined-outer-name
    if not isinstance(date, (datetime.date, datetime.datetime)):
        raise ValueError("date must be a datetime object")
    query = Punchcard.select().where(
        Punchcard.date == date,
    )

    result = list(query.execute())
    return result
