def set_brightness(self, brightness):
        """
        Set the brightness level for the entire display
        @param brightness: brightness level (0 -15)
        """
        if brightness > 15:
            brightness = 15
        brightness |= 0xE0
        self.brightness = brightness
        self.firmata.i2c_write(0x70, brightness)