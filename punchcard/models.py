from datetime import datetime

from peewee import (
    DateField,
    IntegerField,
    Model,
    SqliteDatabase,
    TimeField,
)

from punchcard.constants import DATABASE_PATH, DATE_FORMAT, TIME_FORMAT

db = SqliteDatabase(DATABASE_PATH)


class Punchcard(Model):
    id = IntegerField(null=True, primary_key=True)
    date = DateField(formats=DATE_FORMAT)
    start = TimeField(formats=TIME_FORMAT)
    end = TimeField(formats=TIME_FORMAT, null=True)

    def duration(self) -> float | None:
        """
        Calculate the duration between the start and end times in hours.
        If the card is still in progress and the end time is not set, returns None.

        Returns:
            float | None: The duration in *hours* if the end time is set, otherwise None.
        """
        if self.end is None:
            return None

        return (
            datetime.strptime(self.end, TIME_FORMAT)
            - datetime.strptime(self.start, TIME_FORMAT)
        ).total_seconds() // 3600

    def __str__(self) -> str:
        return (
            f"{self.id} {self.date} {self.start} {self.end} {self.duration()}"
        )

    def __repr__(self) -> str:
        return f"Punchcard(id={self.id}, date={self.date}, start={self.start}, end={self.end})"

    class Meta:
        database = db
