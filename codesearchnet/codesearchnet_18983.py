def output_entire_buffer(self):
        """
        Write the entire buffer to the display
        """
        green = 0
        red = 0

        for row in range(0, 8):
            for col in range(0, 8):
                if self.display_buffer[row][col] == self.LED_GREEN:
                    green |= 1 << col
                elif self.display_buffer[row][col] == self.LED_RED:
                    red |= 1 << col
                elif self.display_buffer[row][col] == self.LED_YELLOW:
                    green |= 1 << col
                    red |= 1 << col
                elif self.display_buffer[row][col] == self.LED_OFF:
                    green &= ~(1 << col)
                    red &= ~(1 << col)

            self.firmata.i2c_write(0x70, row * 2, 0, green)
            self.firmata.i2c_write(0x70, row * 2 + 1, 0, red)