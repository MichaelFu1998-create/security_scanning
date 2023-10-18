def play_tone(self, pin, tone_command, frequency, duration):
        """
        This method will call the Tone library for the selected pin.
        If the tone command is set to TONE_TONE, then the specified tone will be played.
        Else, if the tone command is TONE_NO_TONE, then any currently playing tone will be disabled.
        It is intended for a future release of Arduino Firmata

        :param pin: Pin number

        :param tone_command: Either TONE_TONE, or TONE_NO_TONE

        :param frequency: Frequency of tone in hz

        :param duration: Duration of tone in milliseconds

        :return: No return value
        """

        # convert the integer values to bytes
        if tone_command == self.TONE_TONE:
            # duration is specified
            if duration:
                data = [tone_command, pin, frequency & 0x7f, (frequency >> 7) & 0x7f, duration & 0x7f, (duration >> 7) & 0x7f]

            else:
                data = [tone_command, pin, frequency & 0x7f, (frequency >> 7) & 0x7f, 0, 0]

            self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_MODE] = \
                self.TONE
        # turn off tone
        else:
            data = [tone_command, pin]
        self._command_handler.send_sysex(self._command_handler.TONE_PLAY, data)