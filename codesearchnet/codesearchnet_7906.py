def send(self, message, json=False, callback=None):
        """Use send to send a simple string message.

        If ``json`` is True, the message will be encoded as a JSON object
        on the wire, and decoded on the other side.

        This is mostly for backwards compatibility.  ``emit()`` is more fun.

        :param callback: This is a callback function that will be
                         called automatically by the client upon
                         reception.  It does not verify that the
                         listener over there was completed with
                         success.  It just tells you that the browser
                         got a hold of the packet.
        :type callback: callable
        """
        pkt = dict(type="message", data=message, endpoint=self.ns_name)
        if json:
            pkt['type'] = "json"

        if callback:
            # By passing ack=True, we use the old behavior of being returned
            # an 'ack' packet, automatically triggered by the client-side
            # with no user-code being run.  The emit() version of the
            # callback is more useful I think :)  So migrate your code.
            pkt['ack'] = True
            pkt['id'] = msgid = self.socket._get_next_msgid()
            self.socket._save_ack_callback(msgid, callback)

        self.socket.send_packet(pkt)