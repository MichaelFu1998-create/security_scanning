def write_success_response(self, result):
    """
    Result may be a python dictionary, array or a primitive type
    that can be converted to JSON for writing back the result.
    """
    response = self.make_success_response(result)
    now = time.time()
    spent = now - self.basehandler_starttime
    response[constants.RESPONSE_KEY_EXECUTION_TIME] = spent
    self.write_json_response(response)