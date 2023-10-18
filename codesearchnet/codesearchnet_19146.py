def connect(self):
        """Connect to the server

        :raise ConnectionError: If socket cannot establish a connection

        """
        try:
            logger.info(u'Connecting %s:%d' % (self.host, self.port))
            self.sock.connect((self.host, self.port))
        except socket.error:
            raise ConnectionError()
        self.state = CONNECTED