def set_filter(self, filter_text):
        """
        Set a specified aprs-is filter for this connection
        """
        self.filter = filter_text

        self.logger.info("Setting filter to: %s", self.filter)

        if self._connected:
            self._sendall("#filter %s\r\n" % self.filter)