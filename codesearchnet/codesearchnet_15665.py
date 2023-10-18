def _socket_readlines(self, blocking=False):
        """
        Generator for complete lines, received from the server
        """
        try:
            self.sock.setblocking(0)
        except socket.error as e:
            self.logger.error("socket error when setblocking(0): %s" % str(e))
            raise ConnectionDrop("connection dropped")

        while True:
            short_buf = b''
            newline = b'\r\n'

            select.select([self.sock], [], [], None if blocking else 0)

            try:
                short_buf = self.sock.recv(4096)

                # sock.recv returns empty if the connection drops
                if not short_buf:
                    self.logger.error("socket.recv(): returned empty")
                    raise ConnectionDrop("connection dropped")
            except socket.error as e:
                self.logger.error("socket error on recv(): %s" % str(e))
                if "Resource temporarily unavailable" in str(e):
                    if not blocking:
                        if len(self.buf) == 0:
                            break

            self.buf += short_buf

            while newline in self.buf:
                line, self.buf = self.buf.split(newline, 1)

                yield line