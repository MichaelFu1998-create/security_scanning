def get_socket(self, sessid=''):
        """Return an existing or new client Socket."""

        socket = self.sockets.get(sessid)

        if sessid and not socket:
            return None  # you ask for a session that doesn't exist!
        if socket is None:
            socket = Socket(self, self.config)
            self.sockets[socket.sessid] = socket
        else:
            socket.incr_hits()

        return socket