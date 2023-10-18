def stepper_step(self, motor_speed, number_of_steps):
        """
        Move a stepper motor for the number of steps at the specified speed

        :param motor_speed: 21 bits of data to set motor speed

        :param number_of_steps: 14 bits for number of steps & direction
                                positive is forward, negative is reverse
        """
        if number_of_steps > 0:
            direction = 1
        else:
            direction = 0
        abs_number_of_steps = abs(number_of_steps)
        data = [self.STEPPER_STEP, motor_speed & 0x7f, (motor_speed >> 7) & 0x7f, (motor_speed >> 14) & 0x7f,
                abs_number_of_steps & 0x7f, (abs_number_of_steps >> 7) & 0x7f, direction]
        self._command_handler.send_sysex(self._command_handler.STEPPER_DATA, data)