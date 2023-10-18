def update(self):
        """
        Tells the connection manager to receive the next 1024 byte of messages
        to analyze.
        """
        try:
            self.manager.handle(self.socket.recv(1024))
        except socket.error:
            pass