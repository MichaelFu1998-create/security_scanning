def send(self, command, timeout=5):
        """Send a command to the server

        :param string command: command to send

        """
        logger.info(u'Sending %s' % command)
        _, writable, __ = select.select([], [self.sock], [], timeout)
        if not writable:
            raise SendTimeoutError()
        writable[0].sendall(command + '\n')