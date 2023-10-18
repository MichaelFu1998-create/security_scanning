def servo_config(self, pin, min_pulse=544, max_pulse=2400):
        """
        Configure a pin as a servo pin. Set pulse min, max in ms.

        :param pin: Servo Pin.

        :param min_pulse: Min pulse width in ms.

        :param max_pulse: Max pulse width in ms.

        :return: No return value
        """
        self.set_pin_mode(pin, self.SERVO, self.OUTPUT)
        command = [pin, min_pulse & 0x7f, (min_pulse >> 7) & 0x7f,
                   max_pulse & 0x7f, (max_pulse >> 7) & 0x7f]

        self._command_handler.send_sysex(self._command_handler.SERVO_CONFIG, command)