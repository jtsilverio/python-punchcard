from datetime import datetime
from typing import Tuple

from punchcard.config import DATE_FORMAT, TIME_FORMAT


def now() -> Tuple[str, str]:
    datetime_now = datetime.now()
    date = datetime_now.date().strftime(DATE_FORMAT)
    time = datetime_now.time().strftime(TIME_FORMAT)

    return date, time
