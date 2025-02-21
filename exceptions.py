from rest_framework.views import exception_handler
import re


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 400:
        required_fields = []

        for field, messages in response.data.items():
            if field == "non_field_errors":
                # Handle login error message
                error_msg = messages[0]
                if "Must include" in error_msg:
                    # Extract fields between quotes
                    required_fields.extend(re.findall(r'"([^"]*)"', error_msg))
            else:
                # Handle signup/regular field errors
                if isinstance(messages, list) and any(
                    "This field is required." in msg for msg in messages
                ):
                    required_fields.append(field)

        if required_fields:
            response.data = {"error": f"Please provide: {', '.join(required_fields)}"}

    return response
