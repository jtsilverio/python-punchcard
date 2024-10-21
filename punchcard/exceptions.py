from typing import Any


class PunchcardError(Exception):
    pass


class AlreadyClockedOutError(PunchcardError):
    message = "Already clocked out"

    def __init__(self, *args: Any, message: str | None = None):
        if message is not None:
            self.message = message
        super().__init__(self.message, *args)


class NotClockedOutError(PunchcardError):
    message = "Not clocked out"

    def __init__(self, *args: Any, message: str | None = None):
        if message is not None:
            self.message = message
        super().__init__(self.message, *args)


class NotClockedinError(PunchcardError):
    message = "Not clocked in"

    def __init__(self, *args: Any, message: str | None = None):
        if message is not None:
            self.message = message
        super().__init__(self.message, *args)
