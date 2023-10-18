def __expect(self, exp='> ', timeout=None):
        """will wait for exp to be returned from nodemcu or timeout"""
        timeout_before = self._port.timeout
        timeout = timeout or self._timeout
        #do NOT set timeout on Windows
        if SYSTEM != 'Windows':
            # Checking for new data every 100us is fast enough
            if self._port.timeout != MINIMAL_TIMEOUT:
                self._port.timeout = MINIMAL_TIMEOUT

        end = time.time() + timeout

        # Finish as soon as either exp matches or we run out of time (work like dump, but faster on success)
        data = ''
        while not data.endswith(exp) and time.time() <= end:
            data += self._port.read()

        log.debug('expect returned: `{0}`'.format(data))
        if time.time() > end:
            raise CommunicationTimeout('Timeout waiting for data', data)

        if not data.endswith(exp) and len(exp) > 0:
            raise BadResponseException('Bad response.', exp, data)

        if SYSTEM != 'Windows':
            self._port.timeout = timeout_before

        return data