def set_bit_map(self, shape, color):
        """
        Populate the bit map with the supplied "shape" and color
        and then write the entire bitmap to the display
        @param shape: pattern to display
        @param color: color for the pattern
        """
        for row in range(0, 8):
            data = shape[row]
            # shift data into buffer
            bit_mask = 0x80
            for column in range(0, 8):
                if data & bit_mask:
                    self.set_pixel(row, column, color, True)
                bit_mask >>= 1
        self.output_entire_buffer()