def mpsse_read_gpio(self):
        """Read both GPIO bus states and return a 16 bit value with their state.
        D0-D7 are the lower 8 bits and C0-C7 are the upper 8 bits.
        """
        # Send command to read low byte and high byte.
        self._write('\x81\x83')
        # Wait for 2 byte response.
        data = self._poll_read(2)
        # Assemble response into 16 bit value.
        low_byte = ord(data[0])
        high_byte = ord(data[1])
        logger.debug('Read MPSSE GPIO low byte = {0:02X} and high byte = {1:02X}'.format(low_byte, high_byte))
        return (high_byte << 8) | low_byte