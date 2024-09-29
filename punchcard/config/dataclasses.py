from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class UserConfig:
    workhours: float
    workdays: int
    lunchbreak: float

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        for field in self.__dataclass_fields__.values():  # pylint: disable=no-member
            if not isinstance(getattr(self, field.name), field.type):
                raise TypeError(
                    f"Expected {field.type} for {field.name}, got {type(getattr(self, field.name))}"
                )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserConfig":
        config = cls(
            workhours=float(data["workhours"]),
            workdays=int(data["workdays"]),
            lunchbreak=float(data["lunchbreak"]),
        )
        return config

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def __str__(self) -> str:
        return f"UserConfig(workhours={self.workhours}, workdays={self.workdays}, lunchbreak={self.lunchbreak})"  # pylint: disable=line-too-long
