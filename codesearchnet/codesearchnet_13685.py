def initiate(self, transport, to = None):
        """Initiate an XMPP connection over the `transport`.

        :Parameters:
            - `transport`: an XMPP transport instance
            - `to`: peer name
        """
        with self.lock:
            self.initiator = True
            self.transport = transport
            transport.set_target(self)
            if to:
                self.peer = JID(to)
            else:
                self.peer = None
            if transport.is_connected():
                self._initiate()