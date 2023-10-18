def make_success_response(self, result):
    """
    Makes the python dict corresponding to the
    JSON that needs to be sent for a successful
    response. Result is the actual payload
    that gets sent.
    """
    response = self.make_response(constants.RESPONSE_STATUS_SUCCESS)
    response[constants.RESPONSE_KEY_RESULT] = result
    return response