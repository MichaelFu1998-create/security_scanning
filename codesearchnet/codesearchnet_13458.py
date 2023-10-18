def loop_iteration(self, timeout = 60):
        """A loop iteration - check any scheduled events
        and I/O available and run the handlers.
        """
        next_timeout, sources_handled = self._call_timeout_handlers()
        if self._quit:
            return sources_handled
        if self._timeout is not None:
            timeout = min(timeout, self._timeout)
        if next_timeout is not None:
            timeout = min(next_timeout, timeout)
        for handler in list(self._unprepared_handlers):
            self._configure_io_handler(handler)
        events = self.poll.poll(timeout * 1000)
        self._timeout = None
        for (fileno, event) in events:
            if event & select.POLLHUP:
                self._handlers[fileno].handle_hup()
            if event & select.POLLNVAL:
                self._handlers[fileno].handle_nval()
            if event & select.POLLIN:
                self._handlers[fileno].handle_read()
            elif event & select.POLLERR:
                # if POLLIN was set this condition should be already handled
                self._handlers[fileno].handle_err()
            if event & select.POLLOUT:
                self._handlers[fileno].handle_write()
            sources_handled += 1
            self._configure_io_handler(self._handlers[fileno])
        return sources_handled