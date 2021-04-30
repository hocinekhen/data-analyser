"""Validating the inputes for views"""


from jsonschema import validate

from . import exceptions


def is_columns_in_matrix(matrix, columns):
    """verify if columns exists in the matrix"""
    ordered_matrix_columns = sorted(matrix.columns)
    ordered_columns = sorted(columns)
    is_columns_belong_to_matrix = set(ordered_columns).issubset(
        set(ordered_matrix_columns)
    )
    return is_columns_belong_to_matrix


def check_fields_presence(request_body, fields):
    """
    if one field of the fields is not present in the request_body
    return false, otherwise true.
    """

    body_fields = request_body.keys()
    for field in fields:
        if field not in body_fields:
            error_message = f"field: {field} is required"
            raise exceptions.ValidationError(message=error_message)

    return True


def check_if_columns_belong_to_matrix(matrix, columns):
    """
    check if the matrix contains specified columns
    otherwise, raise ValidationError
    """
    is_columns_included = is_columns_in_matrix(matrix=matrix, columns=columns)
    if not is_columns_included:
        error_message = f"specified columns does not belong to the matrix"
        raise exceptions.ValidationError(message=error_message)


def check_columns_uniqueness(columns):
    """
    check if all elements in columns are not duplicated
    """
    is_columns_unique = len(set(columns)) == len(columns)
    if not is_columns_unique:
        error_message = f"columns should be different"
        raise exceptions.ValidationError(message=error_message)


# Correlation
def validate_correlation_body(request_body):
    """
    validate the body sent for calculation correlation
    """
    schema = {
        "type": "object",
        "properties": {
            "columns": {
                "type": "array",
                "uniqueItems": True,
                "minItems": 1,
            },
            "is_in_body": {"type": "boolean"},
            "matrix": {
                "type": "object",
                "properties": {
                    "matrix": {
                        "type": "array",
                        "items": [{
                            "type": "array"
                        }],
                    },
                    "columns": {
                        "type": "array",
                        "uniqueItems": True,
                    }
                },
                "required": ["matrix", "columns"],
            }
        },
        "required": ["columns", "is_in_body"],
        "if": {
            "properties": {
                "is_in_body": {"const": True}
            }
        },
        "then": {"required": ["matrix"]}
    }
    try:
        validate(instance=request_body, schema=schema)
    except Exception as e:
        error_message = e.message
        raise exceptions.ValidationError(message=error_message)


# Merge
def validate_merge_body(request_body):
    """
    validate the body sent for merging
    """
    schema = {
        "type": "object",
        "properties": {
            "columns_to_merge": {
                "type": "array",
                "uniqueItems": True,
                "minItems": 1,
            },
            "column_name": {
                "type": "string",
            },
            "is_in_body": {"type": "boolean"},
            "matrix": {
                "type": "object",
                "properties": {
                    "matrix": {
                        "type": "array",
                        "items": [{
                            "type": "array"
                        }],
                    },
                    "columns": {
                        "type": "array",
                        "uniqueItems": True,
                    }
                },
                "required": ["matrix", "columns"],
            }
        },
        "required": ["column_name", "columns_to_merge", "is_in_body"],
        "if": {
            "properties": {
                "is_in_body": {"const": True}
            }
        },
        "then": {"required": ["matrix"]}
    }
    try:
        validate(instance=request_body, schema=schema)
    except Exception as e:
        error_message = e.message

        raise exceptions.ValidationError(message=error_message)


# grouping
def validate_group_body(request_body):
    """
    validate the body sent for grouping
    """
    schema = {
        "type": "object",
        "properties": {
            "columns_to_group": {
                "type": "array",
                "uniqueItems": True,
                "minItems": 1,
            },
            "is_in_body": {"type": "boolean"},
            "matrix": {
                "type": "object",
                "properties": {
                    "matrix": {
                        "type": "array",
                        "items": [{
                            "type": "array"
                        }],
                    },
                    "columns": {
                        "type": "array",
                        "uniqueItems": True,
                    }
                },
                "required": ["matrix", "columns"],
            }
        },
        "required": ["columns_to_group", "is_in_body"],
        "if": {
            "properties": {
                "is_in_body": {"const": True}
            }
        },
        "then": {"required": ["matrix"]}
    }
    try:
        validate(instance=request_body, schema=schema)
    except Exception as e:
        error_message = e.message

        raise exceptions.ValidationError(message=error_message)


# Filtering
def validate_filter_body(request_body):
    """
    validate the body sent for grouping
    """
    schema = {
        "type": "object",
        "properties": {
            "column_to_filter": {
                "type": "string",
            },
            "min": {"type": "number"},
            "max": {"type": "number"},
            "is_in_body": {"type": "boolean"},
            "matrix": {
                "type": "object",
                "properties": {
                    "matrix": {
                        "type": "array",
                        "items": [{
                            "type": "array"
                        }],
                    },
                    "columns": {
                        "type": "array",
                        "uniqueItems": True,
                    }
                },
                "required": ["matrix", "columns"],
            }
        },
        "required": ["column_to_filter", "min", "max", "is_in_body"],
        "if": {
            "properties": {
                "is_in_body": {"const": True}
            }
        },
        "then": {"required": ["matrix"]}
    }
    try:
        validate(instance=request_body, schema=schema)
    except Exception as e:
        error_message = e.message

        raise exceptions.ValidationError(message=error_message)


# formatting
def validate_matrix_to_series_body(request_body):
    """
    validate the body sent for grouping
    """
    schema = {
        "type": "object",
        "properties": {
            "column_x": {
                "type": "string",
            },
            "column_y": {"type": "string"},
            "column_values": {"type": "string"},
            "is_in_body": {"type": "boolean"},
            "matrix": {
                "type": "object",
                "properties": {
                    "matrix": {
                        "type": "array",
                        "items": [{
                            "type": "array"
                        }],
                    },
                    "columns": {
                        "type": "array",
                        "uniqueItems": True,
                    }
                },
                "required": ["matrix", "columns"],
            }
        },
        "required": ["column_x", "column_y", "column_values", "is_in_body"],
        "if": {
            "properties": {
                "is_in_body": {"const": True}
            }
        },
        "then": {"required": ["matrix"]}
    }
    try:
        validate(instance=request_body, schema=schema)
    except Exception as e:
        error_message = e.message

        raise exceptions.ValidationError(message=error_message)


# Regression
def validate_regression_body(request_body):
    """
    validate the body sent for calculation correlation
    """
    schema = {
        "type": "object",
        "properties": {
            "columns": {
                "type": "array",
                "uniqueItems": True,
                "minItems": 2,
                "maxItems": 2
            },
            "is_in_body": {"type": "boolean"},
            "matrix": {
                "type": "object",
                "properties": {
                    "matrix": {
                        "type": "array",
                        "items": [{
                            "type": "array"
                        }],
                    },
                    "columns": {
                        "type": "array",
                        "uniqueItems": True,
                    }
                },
                "required": ["matrix", "columns"],
            }
        },
        "required": ["columns", "is_in_body"],
        "if": {
            "properties": {
                "is_in_body": {"const": True}
            }
        },
        "then": {"required": ["matrix"]}
    }
    try:
        validate(instance=request_body, schema=schema)
    except Exception as e:
        error_message = e.message

        raise exceptions.ValidationError(message=error_message)
