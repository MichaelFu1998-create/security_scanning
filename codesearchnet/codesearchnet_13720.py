def prepare(self):
        """When connecting start the next connection step and schedule
        next `prepare` call, when connected return `HandlerReady()`
        """
        with self._lock:
            if self._socket:
                self._socket.listen(SOMAXCONN)
                self._socket.setblocking(False)
            return HandlerReady()