"""
Library-specific exceptions module.

This module contains custom exceptions used throughout the library application
to handle specific error conditions in a structured way.
"""


class DirNotExists(Exception):
    """Exception raised when a required directory does not exist."""

    def __init__(self, message):
        """Initialize the exception with a descriptive message.

        Args:
            message (str): Explanation of the error, typically including the path
                          of the directory that doesn't exist.
        """
        super().__init__(message)


class DownloadError(Exception):
    """Exception raised when a download operation fails."""

    def __init__(self, message: str):
        """Initialize the exception with a descriptive message.

        Args:
            message (str): Explanation of the error,
                           typically including http code and message.
        """
        super().__init__(message)
