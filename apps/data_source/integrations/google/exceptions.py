class GoogleConnectionError(Exception):
    pass


class GoogleServerError(Exception):
    pass


class GoogleSearchConnectionError(GoogleConnectionError):
    pass


class GoogleSearchServerError(GoogleServerError):
    pass
