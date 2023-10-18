def tx(self, message):
        """
        Transmit a series of bytes
        :param message: a list of bytes to send
        :return: None
        """
        message = message if isinstance(message, list) else [message]

        length = len(message)
        length_high_byte = (length & 0xff00) >> 8
        length_low_byte = length & 0x00ff

        message_with_length = [length_low_byte, length_high_byte] + message

        sum1, sum2 = self._fletcher16_checksum(message_with_length)
        message_with_length.append(sum1)
        message_with_length.append(sum2)

        message = [self._START_OF_FRAME]

        for b in message_with_length:
            if b in [self._START_OF_FRAME, self._END_OF_FRAME, self._ESC]:
                message.append(self._ESC)
                message.append(b ^ self._ESC_XOR)
            else:
                message.append(b)

        message.append(self._END_OF_FRAME)

        self._port.write(message)