def connect(self):
        """Schedule a new XMPP c2s connection.
        """
        with self.lock:
            if self.stream:
                logger.debug("Closing the previously used stream.")
                self._close_stream()

            transport = TCPTransport(self.settings)

            addr = self.settings["server"]
            if addr:
                service = None
            else:
                addr = self.jid.domain
                service = self.settings["c2s_service"]

            transport.connect(addr, self.settings["c2s_port"], service)
            handlers = self._base_handlers[:]
            handlers += self.handlers + [self]
            self.clear_response_handlers()
            self.setup_stanza_handlers(handlers, "pre-auth")
            stream = ClientStream(self.jid, self, handlers, self.settings)
            stream.initiate(transport)
            self.main_loop.add_handler(transport)
            self.main_loop.add_handler(stream)
            self._ml_handlers += [transport, stream]
            self.stream = stream
            self.uplink = stream