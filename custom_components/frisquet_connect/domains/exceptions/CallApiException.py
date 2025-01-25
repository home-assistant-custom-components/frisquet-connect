from custom_components.frisquet_connect.domains.exceptions import TechnicalException


class CallApiException(TechnicalException):
    """Exception raised when calling the API"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)