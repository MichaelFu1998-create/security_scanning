def _transaction_end(self):
        """End I2C transaction and get response bytes, including ACKs."""
        # Ask to return response bytes immediately.
        self._command.append('\x87')
        # Send the entire command to the MPSSE.
        self._ft232h._write(''.join(self._command))
        # Read response bytes and return them.
        return bytearray(self._ft232h._poll_read(self._expected))