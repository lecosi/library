class OpenLibraConnectionError(Exception):
    pass


class OpenLibraServerError(Exception):
    pass


class OpenLibraSearchConnectionError(OpenLibraConnectionError):
    pass


class OpenLibraSearchServerError(OpenLibraServerError):
    pass
