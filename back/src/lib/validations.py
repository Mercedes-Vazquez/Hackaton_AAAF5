from src.lib.errors import BadRequestError, NotAuthorizedError
import re


def validate_required_fields(data, required_keys):
    errors = {}
    for required_key in required_keys:
        if required_key not in data:
            errors[required_key] = "REQUIRED"
    if errors:
        raise BadRequestError(errors)


def validate_required_types(data, required_types):
    errors = {}
    for key in data:
        value = data[key]
        required_type = required_types[key]
        if not isinstance(value, required_type):
            errors[key] = "BAD FORMAT"
    if errors:
        raise BadRequestError(errors)


def validate_required_range_of_values(data, range_of_values):
    errors = {}
    for key in data:
        value = data[key]
        if value not in range_of_values:
            errors[key] = "BAD VALUE"
    if errors:
        raise BadRequestError(errors)


def validate_iso8601_timestamp(timestamp):
    regex = r"^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"
    match = re.compile(regex).match(timestamp)
    if match is None:
        raise BadRequestError({"timestamp": "BAD FORMAT"})


def validate_date_format(date):
    regex = r"^(([1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$"
    match = re.compile(regex).match(date)
    if match is None:
        raise BadRequestError({"date": "BAD FORMAT"})


def validate_user_authentication(user):
    if user is None:
        errors = {"msg": "This operation is not authorized. Please, log in."}
        raise NotAuthorizedError(errors)


def validate_admin_role(user):
    if not user.is_admin:
        errors = {"msg": "This operation is not authorized."}
        raise NotAuthorizedError(errors)
