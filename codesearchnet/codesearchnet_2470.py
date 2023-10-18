def make_response(self, status):
    """
    Makes the base dict for the response.
    The status is the string value for
    the key "status" of the response. This
    should be "success" or "failure".
    """
    response = {
        constants.RESPONSE_KEY_STATUS: status,
        constants.RESPONSE_KEY_VERSION: constants.API_VERSION,
        constants.RESPONSE_KEY_EXECUTION_TIME: 0,
        constants.RESPONSE_KEY_MESSAGE: "",
    }
    return response