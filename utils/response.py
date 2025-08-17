from rest_framework.response import Response
from rest_framework import status

def success_response(data, statusCode= status.HTTP_200_OK):
    response = { "success": True, "data": data, "errorCode": None, "erroMsg": "" }
    return Response(response, statusCode)

def failure_response(erroMsg, code, statusCode= status.HTTP_200_OK):
    response = { "success": False, "data": None, "errorCode": code, "erroMsg": erroMsg }
    return Response(response, statusCode)

def get_strutured_error(errors, request_data=None):

    # Take the first error
    field = list(errors.keys())[0]
    error_detail = errors[field][0]  # ErrorDetail
    code = error_detail.code

    # Human-readable field name
    field_readable = field.replace("_", " ").capitalize()

    # Default fallback message
    message = str(error_detail)

    params = getattr(error_detail, "params", {})

    if code in ("required", "blank", "null"):
        message = f"{field_readable} is required"

    elif code == "min_length":
        limit_value = params.get("limit_value")
        if limit_value:
            message = f"{field_readable} should be minimum {limit_value} characters"
        else:
            message = f"{field_readable} is too short"
    elif code == "max_length":
        limit_value = params.get("limit_value")
        if limit_value:
            message = f"{field_readable} should be maximum {limit_value} characters"
        else:
            message = f"{field_readable} is too long"

    elif code == "invalid_choice":
        message = f"Please enter a valid {field_readable}"

    elif code == "unique":
        field_value = ""
        if request_data:
            field_value = request_data.get(field, "")
        message = f"{field_readable} already exists with {field_value}"

    # invalid → just use the default string

    return { "message": message, "error_code": "VALIDATION_ERROR" }
