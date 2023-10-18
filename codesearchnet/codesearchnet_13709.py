def loop_iteration(self, timeout = 60):
        """A loop iteration - check any scheduled events
        and I/O available and run the handlers.
        """
        if self.check_events():
            return 0
        next_timeout, sources_handled = self._call_timeout_handlers()
        if self._quit:
            return sources_handled
        if next_timeout is not None:
            timeout = min(next_timeout, timeout)
        readable, writable, next_timeout = self._prepare_handlers()
        if next_timeout is not None:
            timeout = min(next_timeout, timeout)
        if not readable and not writable:
            readable, writable, _unused = [], [], None
            time.sleep(timeout)
        else:
            logger.debug("select({0!r}, {1!r}, [], {2!r})"
                                    .format( readable, writable,timeout))
            readable, writable, _unused = select.select(
                                            readable, writable, [], timeout)
        for handler in readable:
            handler.handle_read()
            sources_handled += 1
        for handler in writable:
            handler.handle_write()
            sources_handled += 1
        return sources_handled