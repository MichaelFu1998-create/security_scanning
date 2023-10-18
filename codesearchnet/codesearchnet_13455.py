def _configure_io_handler(self, handler):
        """Register an io-handler at the polling object."""
        if self.check_events():
            return
        if handler in self._unprepared_handlers:
            old_fileno = self._unprepared_handlers[handler]
            prepared = self._prepare_io_handler(handler)
        else:
            old_fileno = None
            prepared = True
        fileno = handler.fileno()
        if old_fileno is not None and fileno != old_fileno:
            del self._handlers[old_fileno]
            try:
                self.poll.unregister(old_fileno)
            except KeyError:
                # The socket has changed, but the old one isn't registered,
                # e.g. ``prepare`` wants to connect again
                pass
        if not prepared:
            self._unprepared_handlers[handler] = fileno
        if not fileno:
            return
        self._handlers[fileno] = handler
        events = 0
        if handler.is_readable():
            logger.debug(" {0!r} readable".format(handler))
            events |= select.POLLIN
        if handler.is_writable():
            logger.debug(" {0!r} writable".format(handler))
            events |= select.POLLOUT
        if events:
            logger.debug(" registering {0!r} handler fileno {1} for"
                            " events {2}".format(handler, fileno, events))
            self.poll.register(fileno, events)