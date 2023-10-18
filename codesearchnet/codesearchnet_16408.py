def connection_made(self, transport):
        """ On socket creation """
        self.transport = transport

        sock = transport.get_extra_info("socket")
        self.port = sock.getsockname()[1]