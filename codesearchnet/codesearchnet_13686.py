def receive(self, transport, myname):
        """Receive an XMPP connection over the `transport`.

        :Parameters:
            - `transport`: an XMPP transport instance
            - `myname`: local stream endpoint name.
        """
        with self.lock:
            self.transport = transport
            transport.set_target(self)
            self.me = JID(myname)
            self.initiator = False
            self._setup_stream_element_handlers()