def _parse_raw_data(self):
        """
        Parses the incoming data and determines if it is valid.  Valid
        data gets placed into self._messages
        :return: None
        """
        if self._START_OF_FRAME in self._raw and self._END_OF_FRAME in self._raw:

            while self._raw[0] != self._START_OF_FRAME and len(self._raw) > 0:
                self._raw.pop(0)

            if self._raw[0] == self._START_OF_FRAME:
                self._raw.pop(0)

            eof_index = self._raw.index(self._END_OF_FRAME)
            raw_message = self._raw[:eof_index]
            self._raw = self._raw[eof_index:]

            logger.debug('raw message: {}'.format(raw_message))

            message = self._remove_esc_chars(raw_message)
            logger.debug('message with checksum: {}'.format(message))

            expected_checksum = (message[-1] << 8) | message[-2]
            logger.debug('checksum: {}'.format(expected_checksum))

            message = message[:-2]  # checksum bytes
            logger.debug('message: {}'.format(message))

            sum1, sum2 = self._fletcher16_checksum(message)
            calculated_checksum = (sum2 << 8) | sum1

            if expected_checksum == calculated_checksum:
                message = message[2:]  # remove length
                logger.debug('valid message received: {}'.format(message))
                self._messages.append(message)
            else:
                logger.warning('invalid message received: {}, discarding'.format(message))
                logger.debug('expected checksum: {}, calculated checksum: {}'.format(expected_checksum, calculated_checksum))

        # remove any extra bytes at the beginning
        try:
            while self._raw[0] != self._START_OF_FRAME and len(self._raw) > 0:
                self._raw.pop(0)
        except IndexError:
            pass