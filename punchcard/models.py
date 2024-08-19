from datetime import datetime

import peewee

from punchcard.constants import DATABASE_PATH
from punchcard.exceptions import AlreadyClockedOutError, NotClockedOutError

db = peewee.SqliteDatabase(DATABASE_PATH)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Punchcard(BaseModel):
    id = peewee.AutoField(primary_key=True)
    start = peewee.DateTimeField()
    end = peewee.DateTimeField(null=False, default=None)

    def __str__(self):
        return f"{self.start} - {self.end}"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Punchcard):
            raise ValueError(
                f"Cannot compare Punchcard object with {isinstance(value)} type"
            )

        return self.start == value.start and self.end == value.end

    def clockout(self):
        if self.end is not None:
            raise AlreadyClockedOutError()

        self.end = datetime.now()

    def duration(self):
        if self.end is None:
            raise NotClockedOutError()

        return int((self.end - self.start).total_seconds() / 60)
