def _io_callback(self, fileno, condition, handler):
        """Called by glib on I/O event."""
        # pylint: disable=W0613
        self._anything_done = True
        logger.debug("_io_callback called for {0!r}, cond: {1}".format(handler,
                                                                    condition))
        try:
            if condition & glib.IO_HUP:
                handler.handle_hup()
            if condition & glib.IO_IN:
                handler.handle_read()
            elif condition & glib.IO_ERR:
                handler.handle_err()
            if condition & glib.IO_OUT:
                handler.handle_write()
            if self.check_events():
                return False
        finally:
            self._io_sources.pop(handler, None)
            self._configure_io_handler(handler)
            self._prepare_pending()
        return False