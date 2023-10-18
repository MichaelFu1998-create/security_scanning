def __write(self, output, binary=False):
        """write data on the nodemcu port. If 'binary' is True the debug log
        will show the intended output as hex, otherwise as string"""
        if not binary:
            log.debug('write: %s', output)
        else:
            log.debug('write binary: %s', hexify(output))
        self._port.write(output)
        self._port.flush()