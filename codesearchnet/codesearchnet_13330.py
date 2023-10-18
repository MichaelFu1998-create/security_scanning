def _configure_io_handler(self, handler):
        """Register an io-handler with the glib main loop."""
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
            tag = self._io_sources.pop(handler, None)
            if tag is not None:
                glib.source_remove(tag)
        if not prepared:
            self._unprepared_handlers[handler] = fileno
        if fileno is None:
            logger.debug(" {0!r}.fileno() is None, not polling"
                                                    .format(handler))
            return
        events = 0
        if handler.is_readable():
            logger.debug(" {0!r} readable".format(handler))
            events |= glib.IO_IN | glib.IO_ERR
        if handler.is_writable():
            logger.debug(" {0!r} writable".format(handler))
            events |= glib.IO_OUT | glib.IO_HUP | glib.IO_ERR
        if events:
            logger.debug(" registering {0!r} handler fileno {1} for"
                            " events {2}".format(handler, fileno, events))
            glib.io_add_watch(fileno, events, self._io_callback, handler)