def __write_chunk(self, chunk):
        """formats and sends a chunk of data to the device according
        to transfer protocol"""
        log.debug('writing %d bytes chunk', len(chunk))
        data = BLOCK_START + chr(len(chunk)) + chunk
        if len(chunk) < 128:
            padding = 128 - len(chunk)
            log.debug('pad with %d characters', padding)
            data = data + (' ' * padding)
        log.debug("packet size %d", len(data))
        self.__write(data)
        self._port.flush()
        return self.__got_ack()