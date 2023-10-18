def stop(self, timeout=None):
        """
        Stops a running loop and waits for it to end if timeout is set. Calling a non-running loop is an error.
        :param timeout: time (in seconds) to wait for the loop to end after signalling it. ``None`` is to block till it
        ends.
        :return: True if the loop stopped, False if still stopping.
        """
        assert self.has_started(), "called stop() on a non-active GeventLoop"
        greenlet = self._greenlet if gevent.getcurrent() != self._greenlet else None
        self._stop_event.set()
        if greenlet is not None and timeout is not None:
            greenlet.join(timeout)
            return greenlet.ready
        else:
            return True