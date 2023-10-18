def _continue_connect(self):
        """Continue connecting.

        [called with `lock` acquired]

        :Return: `True` when just connected
        """
        try:
            self._socket.connect(self._dst_addr)
        except socket.error, err:
            logger.debug("Connect error: {0}".format(err))
            if err.args[0] == errno.EISCONN:
                pass
            elif err.args[0] in BLOCKING_ERRORS:
                return None
            elif self._dst_addrs:
                self._set_state("connect")
                return None
            elif self._dst_nameports:
                self._set_state("resolve-hostname")
                return None
            else:
                self._socket.close()
                self._socket = None
                self._set_state("aborted")
                raise
        self._connected()