def run(self):
        """The thread function."""
        # pylint: disable-msg=W0212
        timeout = self.method._pyxmpp_timeout
        recurring = self.method._pyxmpp_recurring
        while not self._quit and timeout is not None:
            if timeout:
                time.sleep(timeout)
            if self._quit:
                break
            ret = self.method()
            if recurring is None:
                timeout = ret
            elif not recurring:
                break