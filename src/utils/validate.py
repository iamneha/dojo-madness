"""Validation utility."""
from src.utils.exceptions import HTTPError


def data_validation(input_data, fields):
    """Validate input data."""
    if not input_data:
        raise HTTPError(400, "{} are required.".format(fields))

    for field in fields:
        if field not in input_data:
            raise HTTPError(400, "{} is required.".format(field))
    return True
