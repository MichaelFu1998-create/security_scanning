def __got_ack(self):
        """Returns true if ACK is received"""
        log.debug('waiting for ack')
        res = self._port.read(1)
        log.debug('ack read %s', hexify(res))
        return res == ACK