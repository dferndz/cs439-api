from rest_framework.exceptions import APIException


class PasswordDoNotMatchException(APIException):
    status_code = 400
    default_detail = 'passwords_do_not_match'
    default_code = 'passwords_do_not_match'


class InvalidEidException(APIException):
    status_code = 400
    default_code = "invalid_eid"
    default_detail = "invalid_eid"
