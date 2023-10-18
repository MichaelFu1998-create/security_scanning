def _loop(self):
        """Main loop - used internally."""
        while True:
            try:
                with uncaught_greenlet_exception_context():
                    self._loop_callback()
            except gevent.GreenletExit:
                break
            if self._stop_event.wait(self._interval):
                break
        self._clear()