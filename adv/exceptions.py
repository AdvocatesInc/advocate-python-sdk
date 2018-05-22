class APIException(Exception):
    """
    Exception for catching a particular set of API Call Errors
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message
