def mpsse_gpio(self):
        """Return command to update the MPSSE GPIO state to the current direction
        and level.
        """
        level_low  = chr(self._level & 0xFF)
        level_high = chr((self._level >> 8) & 0xFF)
        dir_low  = chr(self._direction & 0xFF)
        dir_high = chr((self._direction >> 8) & 0xFF)
        return str(bytearray((0x80, level_low, dir_low, 0x82, level_high, dir_high)))