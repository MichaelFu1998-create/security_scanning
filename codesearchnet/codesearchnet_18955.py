def encoder_config(self, pin_a, pin_b, cb=None):
        """
        This command enables the rotary encoder (2 pin + ground) and will
        enable encoder reporting.

        NOTE: This command is not currently part of standard arduino firmata, but is provided for legacy
        support of CodeShield on an Arduino UNO.

        Encoder data is retrieved by performing a digital_read from pin a (encoder pin 1)

        :param pin_a: Encoder pin 1.

        :param pin_b: Encoder pin 2.

        :param cb: callback function to report encoder changes

        :return: No return value
        """
        data = [pin_a, pin_b]
        self._command_handler.digital_response_table[pin_a][self._command_handler.RESPONSE_TABLE_MODE] \
            = self.ENCODER
        self._command_handler.digital_response_table[pin_a][self._command_handler.RESPONSE_TABLE_CALLBACK] = cb
        self.enable_digital_reporting(pin_a)

        self._command_handler.digital_response_table[pin_b][self._command_handler.RESPONSE_TABLE_MODE] \
            = self.ENCODER
        self._command_handler.digital_response_table[pin_b][self._command_handler.RESPONSE_TABLE_CALLBACK] = cb
        self.enable_digital_reporting(pin_b)

        self._command_handler.send_sysex(self._command_handler.ENCODER_CONFIG, data)