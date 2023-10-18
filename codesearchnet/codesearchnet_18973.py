def sonar_config(self, trigger_pin, echo_pin, cb=None, ping_interval=50, max_distance=200):
        """
        Configure the pins,ping interval and maximum distance for an HC-SR04 type device.
        Single pin configuration may be used. To do so, set both the trigger and echo pins to the same value.
        Up to a maximum of 6 SONAR devices is supported
        If the maximum is exceeded a message is sent to the console and the request is ignored.
        NOTE: data is measured in centimeters

        :param trigger_pin: The pin number of for the trigger (transmitter).

        :param echo_pin: The pin number for the received echo.

        :param ping_interval: Minimum interval between pings. Lowest number to use is 33 ms.Max is 127

        :param max_distance: Maximum distance in cm. Max is 200.

        :param cb: optional callback function to report sonar data changes
        """
        if max_distance > 200:
            max_distance = 200
        max_distance_lsb = max_distance & 0x7f
        max_distance_msb = (max_distance >> 7) & 0x7f
        data = [trigger_pin, echo_pin, ping_interval, max_distance_lsb, max_distance_msb]
        self.set_pin_mode(trigger_pin, self.SONAR, self.INPUT)
        self.set_pin_mode(echo_pin, self.SONAR, self.INPUT)
        # update the ping data map for this pin
        if len(self._command_handler.active_sonar_map) > 6:
            if self.verbose:
                print("sonar_config: maximum number of devices assigned - ignoring request")
            return
        else:
            with self.data_lock:

                # self._command_handler.active_sonar_map[trigger_pin] = self.IGNORE
                self._command_handler.active_sonar_map[trigger_pin] = [cb, [self.IGNORE]]
        self._command_handler.send_sysex(self._command_handler.SONAR_CONFIG, data)