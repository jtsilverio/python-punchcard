from datetime import datetime

from peewee import (
    DateField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TimeField,
)

from punchcard.config import (
    DATABASE_PATH,
    DATE_FORMAT,
    TIME_FORMAT,
    USER_CONFIG,
)

db = SqliteDatabase(DATABASE_PATH)


class Punchcard(Model):
    id = IntegerField(null=True, primary_key=True)
    date = DateField(formats=DATE_FORMAT)
    entries = ForeignKeyField("Entry", backref="punchcard")

    def duration(self) -> float:
        """
        Calculate the balance of the punchcard by summing the duration of all entries.

        Returns:
            float: The balance in *hours*.
        """
        duration = sum((entry.duration() for entry in self.entries))
        return float(duration)

    def balance(self) -> float:
        """
        Calculate the balance of the punchcard by summing the duration of all entries.

        Returns:
            float: The balance in *hours*.
        """
        return float(self.duration() - USER_CONFIG["workhours"])

    class Meta:
        database = db


class Entry(Model):
    id = IntegerField(null=True, primary_key=True)
    punchcard = ForeignKeyField(Punchcard, backref="entries")
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
        return f"Entry: {self.id} {self.start} {self.end} {self.duration()}"

    def __repr__(self) -> str:
        return f"Entry(id={self.id}, punchcard={self.punchcard} start={self.start}, end={self.end})"

    class Meta:
        database = db
