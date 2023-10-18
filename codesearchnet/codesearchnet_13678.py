def _add_io_handler(self, handler):
        """Add an I/O handler to the loop."""
        logger.debug('adding io handler: %r', handler)
        self._unprepared_handlers[handler] = None
        self._configure_io_handler(handler)