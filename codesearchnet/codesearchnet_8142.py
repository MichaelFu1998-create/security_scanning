def set_device_brightness(self, val):
        """
        APA102 & SK9822 support on-chip brightness control, allowing greater
        color depth.

        APA102 superimposes a 440Hz PWM on the 19kHz base PWM to control
        brightness. SK9822 uses a base 4.7kHz PWM but controls brightness with a
        variable current source.

        Because of this SK9822 will have much less flicker at lower levels.
        Either way, this option is better and faster than scaling in
        BiblioPixel.
        """
        # bitshift to scale from 8 bit to 5
        self._chipset_brightness = (val >> 3)
        self._brightness_list = [0xE0 + self._chipset_brightness] * self.numLEDs
        self._packet[self._start_frame:self._pixel_stop:4] = (
            self._brightness_list)