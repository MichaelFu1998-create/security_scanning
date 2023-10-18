def handle_timeout(self, reqid):
    """Handles timeout"""
    if reqid in self.context_map:
      context = self.context_map.pop(reqid)
      self.response_message_map.pop(reqid)
      self.on_response(StatusCode.TIMEOUT_ERROR, context, None)