def _send_to_consumer(self, block):
        """ Send a block of bytes to the consumer.

        Args:
            block (str): Block of bytes
        """
        self._consumer.write(block)
        self._sent += len(block)
        if self._callback:
            self._callback(self._sent, self.length)