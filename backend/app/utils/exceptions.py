

class AppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundException(AppException):
    pass


class AlreadyExistsException(AppException):
    pass


class UnauthorizedException(AppException):
    pass


class ForbiddenException(AppException):
    pass


class ValidationException(AppException):
    pass
