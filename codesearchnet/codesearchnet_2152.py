def disconnect(self):
        """
        Ends our server tcp connection.
        """
        # If we are not connected, return error.
        if not self.socket:
            logging.warning("No active socket to close!")
            return
        # Close our socket.
        self.socket.close()
        self.socket = None