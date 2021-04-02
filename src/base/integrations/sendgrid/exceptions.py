class SendgridBaseException(Exception):
    pass


class SendgridAuthenticationFailed(SendgridBaseException):
    pass


class SendgridWrongResponse(SendgridBaseException):
    pass
