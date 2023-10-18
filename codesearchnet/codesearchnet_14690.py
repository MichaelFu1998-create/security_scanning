def write_file(self, path, destination='', verify='none'):
        """sends a file to the device using the transfer protocol"""
        filename = os.path.basename(path)
        if not destination:
            destination = filename

        log.info('Transferring %s as %s', path, destination)
        self.__writeln("recv()")

        res = self.__expect('C> ')
        if not res.endswith('C> '):
            log.error('Error waiting for esp "%s"', res)
            raise CommunicationTimeout('Error waiting for device to start receiving', res)

        log.debug('sending destination filename "%s"', destination)
        self.__write(destination + '\x00', True)
        if not self.__got_ack():
            log.error('did not ack destination filename')
            raise NoAckException('Device did not ACK destination filename')

        content = from_file(path)

        log.debug('sending %d bytes in %s', len(content), filename)
        pos = 0
        chunk_size = 128
        while pos < len(content):
            rest = len(content) - pos
            if rest > chunk_size:
                rest = chunk_size

            data = content[pos:pos+rest]
            if not self.__write_chunk(data):
                resp = self.__expect()
                log.error('Bad chunk response "%s" %s', resp, hexify(resp))
                raise BadResponseException('Bad chunk response', ACK, resp)

            pos += chunk_size

        log.debug('sending zero block')
        #zero size block
        self.__write_chunk('')
        if verify != 'none':
            self.verify_file(path, destination, verify)