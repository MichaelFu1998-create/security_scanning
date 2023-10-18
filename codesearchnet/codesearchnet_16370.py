def validate_response(expected_responses):
    """ Decorator to validate responses from QTM """

    def internal_decorator(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):

            response = await function(*args, **kwargs)

            for expected_response in expected_responses:
                if response.startswith(expected_response):
                    return response

            raise QRTCommandException(
                "Expected %s but got %s" % (expected_responses, response)
            )

        return wrapper

    return internal_decorator