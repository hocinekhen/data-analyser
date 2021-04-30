"""Contains the customized exceptions"""


class ValidationError(Exception):
    """Validation Error that will be raised in input validation errors"""

    def __init__(self, message="Validation Error!"):
        self.message = message
        super().__init__(self.message)
