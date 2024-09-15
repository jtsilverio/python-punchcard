from unittest import mock

import pytest

from punchcard.cards import clockout
from punchcard.exceptions import AlreadyClockedOutError
from punchcard.models import Punchcard


def test_punchcard_when_end_is_none():
    date = "2024-01-01"
    start = "12:00"
    punchcard = Punchcard(date=date, start=start)

    assert punchcard.start == start
    assert punchcard.end is None


def test_punchcard_with_end_time():
    date = "2024-01-01"
    start = "12:00"
    end = "13:00"

    punchcard = Punchcard(date=date, start=start, end=end)

    assert punchcard.start == start
    assert punchcard.end == end


def test_punchcard_clockout():
    date = "2024-01-01"
    start = "12:00"

    with mock.patch("punchcard.cards.Punchcard.save") as mock_save:
        punchcard = Punchcard(date=date, start=start)
        clockout(punchcard)

        assert punchcard.end is not None
        assert mock_save.called


def test_clockout_raises_error_when_punchcard_already_clocked_out():
    date = "2024-01-01"
    start = "12:00"
    end = "13:00"

    with mock.patch("punchcard.cards.Punchcard.save") as mock_save:  # pylint: disable=unused-variable
        with pytest.raises(AlreadyClockedOutError):
            punchcard = Punchcard(date=date, start=start, end=end)
            clockout(punchcard)


def test_punchcard_duration():
    date = "2024-01-01"
    start = "12:00"
    end = "13:00"
    punchcard = Punchcard(date=date, start=start, end=end)

    assert punchcard.duration() == 1


def test_duration_returns_none_when_punchcard_not_clocked_out():
    date = "2024-01-01"
    start = "12:00"
    punchcard = Punchcard(date=date, start=start)

    assert punchcard.duration() is None
