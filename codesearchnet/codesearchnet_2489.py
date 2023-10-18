def send_message(self, message):
    """Sends a message (REQID is zero)"""
    Log.debug("In send_message() of %s" % self._get_classname())
    outgoing_pkt = OutgoingPacket.create_packet(REQID.generate_zero(), message)
    self._send_packet(outgoing_pkt)