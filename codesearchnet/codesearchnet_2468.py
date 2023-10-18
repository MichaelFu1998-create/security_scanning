def write_error_response(self, message):
    """
    Writes the message as part of the response and sets 404 status.
    """
    self.set_status(404)
    response = self.make_error_response(str(message))
    now = time.time()
    spent = now - self.basehandler_starttime
    response[constants.RESPONSE_KEY_EXECUTION_TIME] = spent
    self.write_json_response(response)