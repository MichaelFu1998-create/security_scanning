def stepper_config(self, steps_per_revolution, stepper_pins):
        """
        Configure stepper motor prior to operation.

        :param steps_per_revolution: number of steps per motor revolution

        :param stepper_pins: a list of control pin numbers - either 4 or 2
        """
        data = [self.STEPPER_CONFIGURE, steps_per_revolution & 0x7f, (steps_per_revolution >> 7) & 0x7f]
        for pin in range(len(stepper_pins)):
            data.append(stepper_pins[pin])
        self._command_handler.send_sysex(self._command_handler.STEPPER_DATA, data)