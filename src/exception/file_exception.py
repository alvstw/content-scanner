from src.exception.app_exception import AppException


class PathNotFoundException(AppException):
    pass


class PermissionDeniedException(AppException):
    pass


class IOException(AppException):
    pass
