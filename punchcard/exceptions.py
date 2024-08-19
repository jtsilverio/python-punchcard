class AlreadyClockedOutError(Exception):
    message = "Punchcard has already been clocked out"

    def __init__(self, *args, message=None):
        if message is not None:
            self.message = message
        super().__init__(self.message, *args)


class NotClockedOutError(Exception):
    message = "Punchcard has not been clocked out"

    def __init__(self, *args, message=None):
        if message is not None:
            self.message = message
        super().__init__(self.message, *args)


if __name__ == "__main__":
    raise AlreadyClockedOutError()
