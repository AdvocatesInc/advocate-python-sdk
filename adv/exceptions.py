class AdvException(Exception):
    """
    Base exception so that all Advocate SDK Exceptions can be caught be a single root exception if necessary
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class APIException(AdvException):
    """
    Exception for catching communication errors with the Advocate API
    """
    pass


class UpdateError(AdvException):
    """
    Called when an attempt to create or update an object (Widget, DCTA, etc) fails
    """
    pass


class RenderError(AdvException):
    """
    Called when a render fails
    """
    pass
