from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail

def custom_exception_handler(exc, context):
    """Custom exception handler for consistent error responses"""
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data

        # Handle ErrorDetail directly
        if isinstance(data, ErrorDetail):
            response.data = {"error": str(data)}

        # Handle {"error": ErrorDetail(...)} or {"field": [ErrorDetail(...)]} etc.
        elif isinstance(data, dict):
            # If "error" key is present, normalize it
            if "error" in data:
                err_val = data["error"]
                if isinstance(err_val, list) and len(err_val) > 0:
                    err_val = err_val[0]
                if isinstance(err_val, ErrorDetail):
                    err_val = str(err_val)
                response.data = {"error": err_val}

            # Handle field-based errors like {"email": ["user already exists."]}
            elif any(isinstance(v, (list, dict, ErrorDetail)) for v in data.values()):
                first_value = next(iter(data.values()))
                if isinstance(first_value, list):
                    first_value = first_value[0]
                if isinstance(first_value, ErrorDetail):
                    first_value = str(first_value)
                response.data = {"error": first_value}

            # Handle {"detail": "..."} pattern
            elif "detail" in data:
                detail = data["detail"]
                response.data = {"error": str(detail)}

        # Handle any other type of exception payload
        else:
            response.data = {"error": str(data)}

    # if response is not None:
    #     print(exc.detail)
    #     # print(response.data['error'])
    #     # print({'error': list(response.data.values())[0]})
    #     custom_response_data = {
    #         'error': response.data.get('detail') or str(exc)
    #     }
    #
    #     if hasattr(exc, 'get_codes'):
    #         custom_response_data['code'] = exc.get_codes()
    #
    #     response.data = custom_response_data

    return response