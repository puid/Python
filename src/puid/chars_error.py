class CharsError(Exception):
    """Base class for Chars Errors"""

    pass


class InvalidChars(CharsError):
    """Raised when characters string contains invalid character"""

    pass


# class NotValidChars(CharsError):
#     """Raised when value is not an instance of ValidChars"""

#     pass


class NonUniqueChars(CharsError):
    """Raised when characters string contains duplicate characters"""

    pass


class TooFewChars(CharsError):
    """Raised when characters string contains too few characters"""

    pass


class TooManyChars(CharsError):
    """Raised when characters string contains too many characters"""

    pass
