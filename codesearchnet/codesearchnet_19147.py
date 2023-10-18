def disconnect(self):
        """Disconnect from the server"""
        logger.info(u'Disconnecting')
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.state = DISCONNECTED