def kill(self):
        """Kills the running loop and waits till it gets killed."""
        assert self.has_started(), "called kill() on a non-active GeventLoop"
        self._stop_event.set()
        self._greenlet.kill()
        self._clear()