def auth_timeout(self):
        """Handle legacy authentication timeout.

        [client only]"""
        self.lock.acquire()
        try:
            self.__logger.debug("Timeout while waiting for jabber:iq:auth result")
            if self._auth_methods_left:
                self._auth_methods_left.pop(0)
        finally:
            self.lock.release()