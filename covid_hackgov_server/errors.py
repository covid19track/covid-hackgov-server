class CovidHackgovError(Exception):
    """Base class for covid_hackgov_server errors"""

    status_code = 500

    @property
    def message(self):
        try:
            return self.args[0]
        except IndexError:
            return repr(self)

    @property
    def json(self):
        try:
            return self.args[1]
        except IndexError:
            return {}


class BadRequest(CovidHackgovError):
    status_code = 400


class Unauthorized(CovidHackgovError):
    status_code = 401


class Forbidden(CovidHackgovError):
    status_code = 403


class NotFound(CovidHackgovError):
    status_code = 404


class Ratelimited(CovidHackgovError):
    status_code = 429
