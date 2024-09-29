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

    def duration(self) -> float:
        """
        Calculate the balance of the punchcard by summing the duration of all entries.

        Returns:
            float: The balance in *hours*.
        """
        duration = sum((entry.duration() for entry in self.entries))  # pylint: disable=no-member # using peewee backref
        return float(duration)

    def balance(self) -> float:
        """
        Calculate the balance of the punchcard by summing the duration of all entries.

        Returns:
            float: The balance in *hours*.
        """
        return float(self.duration() - USER_CONFIG["workhours"])

    def __str__(self) -> str:
        return f"Punchcard: {self.id} {self.date} {self.duration()}"

    class Meta:
        database = db


class Entry(Model):
    id = IntegerField(null=True, primary_key=True)
    start_time = TimeField(formats=TIME_FORMAT)
    end_time = TimeField(formats=TIME_FORMAT, null=True)
    punchcard = ForeignKeyField(Punchcard, backref="entries")

    def duration(self) -> float | None:
        """
        Calculate the duration between the start and end times in hours.
        If the card is still in progress and the end time is not set, returns None.

        Returns:
            float | None: The duration in *hours* if the end time is set, otherwise None.
        """
        if self.end_time is None:
            return 0.0

        return (
            datetime.strptime(self.end_time, TIME_FORMAT)
            - datetime.strptime(self.start_time, TIME_FORMAT)
        ).total_seconds() // 3600

    def __str__(self) -> str:
        return f"Entry: {self.id} {self.start_time} {self.end_time} {self.duration()}"

    def __repr__(self) -> str:
        return f"Entry(id={self.id}, punchcard={self.punchcard} start={self.start_time}, end={self.end_time})"  # pylint: disable=line-too-long

    class Meta:
        database = db


def initialize_database() -> None:
    db.connect()
    db.create_tables([Punchcard, Entry])


initialize_database()
