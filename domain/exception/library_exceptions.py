"""
Library-specific exceptions module.

This module contains custom exceptions used throughout the library application
to handle specific error conditions in a structured way.
"""


class DirNotExists(Exception):
    """Exception raised when a required directory does not exist.

    Attributes:
        message (str): Explanation of the error, typically including the path
                      of the directory that doesn't exist.
    """

    def __init__(self, message):
        """Initialize the exception with a descriptive message.

        Args:
            message (str): Explanation of the error, typically including the path
                          of the directory that doesn't exist.
        """
        super().__init__(message)


class DownloadError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
