def _handle_register_response(self, response):
    """Called when a register response (RegisterInstanceResponse) arrives"""
    if response.status.status != common_pb2.StatusCode.Value("OK"):
      raise RuntimeError("Stream Manager returned a not OK response for register")
    Log.info("We registered ourselves to the Stream Manager")

    self.is_registered = True
    if response.HasField("pplan"):
      Log.info("Handling assignment message from response")
      self._handle_assignment_message(response.pplan)
    else:
      Log.debug("Received a register response with no pplan")