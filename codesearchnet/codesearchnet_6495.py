def set_color(self, r, g, b):
        """Set the red, green, blue color of the bulb."""
        # See more details on the bulb's protocol from this guide:
        #   https://learn.adafruit.com/reverse-engineering-a-bluetooth-low-energy-light-bulb/overview
        command = '\x58\x01\x03\x01\xFF\x00{0}{1}{2}'.format(chr(r & 0xFF),
                                                             chr(g & 0xFF),
                                                             chr(b & 0xFF))
        self._color.write_value(command)