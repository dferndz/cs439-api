from rest_framework import exceptions


class DuplicateRegradeException(exceptions.APIException):
    status_code = 400
    default_detail = "regrade_already_exists"
    default_code = "regrade_already_exists"


class InvalidCodeException(exceptions.APIException):
    status_code = 401
    default_code = "invalid_code"
    default_detail = "invalid_code"
