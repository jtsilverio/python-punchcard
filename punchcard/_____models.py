from datetime import datetime

from attrs import converters, define, field, validators

from punchcard.exceptions import AlreadyClockedOutError, NotClockedOutError


def datetime_converter(value: datetime) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError("Value must be a datetime object")
    return value.replace(second=0, microsecond=0)


@define
class Punchcard:
    start: datetime = field(
        validator=validators.instance_of(datetime),
        converter=datetime_converter,
    )
    end: datetime = field(
        default=None,
        validator=validators.optional(validators.instance_of(datetime)),
        converter=converters.optional(datetime_converter),
    )
    sqliteid: int = field(
        default=None,
        validator=validators.optional(validators.instance_of(int)),
    )

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
