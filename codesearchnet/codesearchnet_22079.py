def start(self):
        """
        Starts the loop. Calling a running loop is an error.
        """
        assert not self.has_started(), "called start() on an active GeventLoop"
        self._stop_event = Event()
        # note that we don't use safe_greenlets.spawn because we take care of it in _loop by ourselves
        self._greenlet = gevent.spawn(self._loop)