def __read_chunk(self, buf):
        """Read a chunk of data"""
        log.debug('reading chunk')
        timeout_before = self._port.timeout
        if SYSTEM != 'Windows':
            # Checking for new data every 100us is fast enough
            if self._port.timeout != MINIMAL_TIMEOUT:
                self._port.timeout = MINIMAL_TIMEOUT

        end = time.time() + timeout_before

        while len(buf) < 130 and time.time() <= end:
            buf = buf + self._port.read()

        if buf[0] != BLOCK_START or len(buf) < 130:
            log.debug('buffer binary: %s ', hexify(buf))
            raise Exception('Bad blocksize or start byte')

        if SYSTEM != 'Windows':
            self._port.timeout = timeout_before

        chunk_size = ord(buf[1])
        data = buf[2:chunk_size+2]
        buf = buf[130:]
        return (data, buf)