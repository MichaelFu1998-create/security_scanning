def send_command(self, command):
        """
        This method is used to transmit a non-sysex command.

        :param command: Command to send to firmata includes command + data formatted by caller

        :return : No return value.
        """
        send_message = ""
        for i in command:
            send_message += chr(i)

        for data in send_message:
            self.pymata.transport.write(data)