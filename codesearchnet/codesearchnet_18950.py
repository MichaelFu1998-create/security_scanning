def digital_write(self, pin, value):
        """
        Set the specified pin to the specified value.

        :param pin: pin number

        :param value: pin value

        :return: No return value
        """
        # The command value is not a fixed value, but needs to be calculated using the
        # pin's port number
        #
        #
        port = pin // 8

        calculated_command = self._command_handler.DIGITAL_MESSAGE + port
        mask = 1 << (pin % 8)
        # Calculate the value for the pin's position in the port mask
        if value == 1:
            self.digital_output_port_pins[port] |= mask

        else:
            self.digital_output_port_pins[port] &= ~mask

        # Assemble the command
        command = (calculated_command, self.digital_output_port_pins[port] & 0x7f,
                   (self.digital_output_port_pins[port] >> 7) & 0x7f)

        self._command_handler.send_command(command)