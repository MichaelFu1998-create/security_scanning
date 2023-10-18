def auth_finish(self, _unused):
        """Handle success of the legacy authentication."""
        self.lock.acquire()
        try:
            self.__logger.debug("Authenticated")
            self.authenticated=True
            self.state_change("authorized",self.my_jid)
            self._post_auth()
        finally:
            self.lock.release()