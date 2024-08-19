from datetime import datetime

import pytest

from punchcard.exceptions import AlreadyClockedOutError, NotClockedOutError
from punchcard.models import Punchcard


def test_punchcard_when_end_is_none():
    start = datetime(2024, 1, 1, 12, 0)
    end = None
    punchcard = Punchcard(start, end)

    assert punchcard.start == start
    assert punchcard.end == end
    assert str(punchcard) == "2024-01-01 12:00:00 - None"


def test_punchcard_with_end_time():
    start = datetime(2024, 1, 1, 12, 0)
    end = datetime(2024, 1, 1, 13, 0)
    punchcard = Punchcard(start, end)

    assert punchcard.start == start
    assert punchcard.end == end
    assert str(punchcard) == "2024-01-01 12:00:00 - 2024-01-01 13:00:00"


def test_punchcard_clockout():
    start = datetime(2024, 1, 1, 12, 0)
    end = None
    punchcard = Punchcard(start, end)

    punchcard.clockout()

    assert punchcard.end is not None
    assert isinstance(punchcard.end, datetime)


def test_punchcard_duration():
    start = datetime(2024, 1, 1, 12, 0)
    end = datetime(2024, 1, 1, 13, 0)
    punchcard = Punchcard(start, end)

    assert punchcard.duration() == 60


def test_duration_raises_error_when_punchcard_not_clocked_out():
    start = datetime(2024, 1, 1, 12, 0)
    end = None
    punchcard = Punchcard(start, end)

    with pytest.raises(NotClockedOutError):
        punchcard.duration()


def test_clockout_raises_error_when_punchcard_already_clocked_out():
    start = datetime(2024, 1, 1, 12, 0)
    end = datetime(2024, 1, 1, 13, 0)
    punchcard = Punchcard(start, end)

    with pytest.raises(AlreadyClockedOutError):
        punchcard.clockout()
