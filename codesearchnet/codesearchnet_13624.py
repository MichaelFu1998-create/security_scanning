def prepare(self):
        """When connecting start the next connection step and schedule
        next `prepare` call, when connected return `HandlerReady()`
        """
        result = HandlerReady()
        logger.debug("TCPTransport.prepare(): state: {0!r}".format(self._state))
        with self.lock:
            if self._state in ("connected", "closing", "closed", "aborted"):
                # no need to call prepare() .fileno() is stable
                pass
            elif self._state == "connect":
                self._start_connect()
                result = PrepareAgain(None)
            elif self._state == "resolve-hostname":
                self._resolve_hostname()
                result = PrepareAgain(0)
            elif self._state == "resolve-srv":
                self._resolve_srv()
                result = PrepareAgain(0)
            else:
                # wait for i/o, but keep calling prepare()
                result = PrepareAgain(None)
        logger.debug("TCPTransport.prepare(): new state: {0!r}"
                                                        .format(self._state))
        return result