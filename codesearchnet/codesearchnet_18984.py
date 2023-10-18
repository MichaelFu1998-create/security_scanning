def clear_display_buffer(self):
        """
        Set all led's to off.
        """
        for row in range(0, 8):
            self.firmata.i2c_write(0x70, row * 2, 0, 0)
            self.firmata.i2c_write(0x70, (row * 2) + 1, 0, 0)

            for column in range(0, 8):
                self.display_buffer[row][column] = 0