def send_request(self, request, context, response_type, timeout_sec):
    """Sends a request message (REQID is non-zero)"""
    # generates a unique request id
    reqid = REQID.generate()
    Log.debug("%s: In send_request() with REQID: %s" % (self._get_classname(), str(reqid)))
    # register response message type
    self.response_message_map[reqid] = response_type
    self.context_map[reqid] = context

    # Add timeout for this request if necessary
    if timeout_sec > 0:
      def timeout_task():
        self.handle_timeout(reqid)
      self.looper.register_timer_task_in_sec(timeout_task, timeout_sec)

    outgoing_pkt = OutgoingPacket.create_packet(reqid, request)
    self._send_packet(outgoing_pkt)