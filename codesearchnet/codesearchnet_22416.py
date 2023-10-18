def wait(self, timeout=None):
        """
        Wait for response until timeout.
        If timeout is specified to None, ``self.timeout`` is used.

        :param float timeout: seconds to wait I/O
        """
        if timeout is None:
            timeout = self._timeout
        while self._process.check_readable(timeout):
            self._flush()