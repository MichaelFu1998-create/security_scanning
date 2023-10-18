def set_blink_rate(self, b):
        """
        Set the user's desired blink rate (0 - 3)
        @param b: blink rate
        """
        if b > 3:
            b = 0  # turn off if not sure
        self.firmata.i2c_write(self.board_address,
                               (self.HT16K33_BLINK_CMD | self.HT16K33_BLINK_DISPLAYON | (b << 1)))