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
            # remove_handler won't raise something like KeyError if the fd
            # isn't registered; it will just print a debug log.
            self.io_loop.remove_handler(old_fileno)
        if not prepared:
            self._unprepared_handlers[handler] = fileno
        if not fileno:
            return
        update = fileno in self._handlers
        events = ioloop.IOLoop.NONE
        if handler.is_readable():
            logger.debug(" {0!r} readable".format(handler))
            events |= ioloop.IOLoop.READ
        if handler.is_writable():
            logger.debug(" {0!r} writable".format(handler))
            events |= ioloop.IOLoop.WRITE

        if self._handlers.get(fileno, None) == events:
            return
        self._handlers[fileno] = events
        if events:
            logger.debug(" registering {0!r} handler fileno {1} for"
                            " events {2}".format(handler, fileno, events))
            if update:
                self.io_loop.update_handler(fileno, events)
            else:
                self.io_loop.add_handler(
                    fileno, partial(self._handle_event, handler), events
                )