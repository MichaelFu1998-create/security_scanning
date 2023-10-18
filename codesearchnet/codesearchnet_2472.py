def make_error_response(self, message):
    """
    Makes the python dict corresponding to the
    JSON that needs to be sent for a failed
    response. Message is the message that is
    sent as the reason for failure.
    """
    response = self.make_response(constants.RESPONSE_STATUS_FAILURE)
    response[constants.RESPONSE_KEY_MESSAGE] = message
    return response