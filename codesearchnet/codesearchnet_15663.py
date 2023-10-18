def _connect(self):
        """
        Attemps connection to the server
        """

        self.logger.info("Attempting connection to %s:%s", self.server[0], self.server[1])

        try:
            self._open_socket()

            peer = self.sock.getpeername()

            self.logger.info("Connected to %s", str(peer))

            # 5 second timeout to receive server banner
            self.sock.setblocking(1)
            self.sock.settimeout(5)

            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            banner = self.sock.recv(512)
            if is_py3:
                banner = banner.decode('latin-1')

            if banner[0] == "#":
                self.logger.debug("Banner: %s", banner.rstrip())
            else:
                raise ConnectionError("invalid banner from server")

        except ConnectionError as e:
            self.logger.error(str(e))
            self.close()
            raise
        except (socket.error, socket.timeout) as e:
            self.close()

            self.logger.error("Socket error: %s" % str(e))
            if str(e) == "timed out":
                raise ConnectionError("no banner from server")
            else:
                raise ConnectionError(e)

        self._connected = True