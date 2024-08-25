class PunchcardError(Exception): ...


class AlreadyClockedOutError(PunchcardError):
    message = "Already clocked out"

    def __init__(self, *args, message=None):
        if message is not None:
            self.message = message
        super().__init__(self.message, *args)


class NotClockedOutError(PunchcardError):
    message = "Already clocked in"

    def __init__(self, *args, message=None):
        if message is not None:
            self.message = message
        super().__init__(self.message, *args)
