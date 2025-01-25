from custom_components.frisquet_connect.domains.exceptions import TechnicalException


class ForbiddenAccessException(TechnicalException):
    """Exception raised when the user is not allowed to access the resource"""

    def __init__(self, message):
        super().__init__(message)
