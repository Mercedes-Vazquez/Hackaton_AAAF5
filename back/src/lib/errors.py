class ApplicationError(Exception):
    def __init__(self, data):
        self.data = data


class BadRequestError(ApplicationError):
    status_code = 400


class NotAuthorizedError(ApplicationError):
    status_code = 401


class ForbiddenError(ApplicationError):
    status_code = 403


class NotFoundError(ApplicationError):
    status_code = 404
