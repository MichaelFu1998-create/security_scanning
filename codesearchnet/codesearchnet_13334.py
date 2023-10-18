def _prepare_io_handler_cb(self, handler):
        """Timeout callback called to try prepare an IOHandler again."""
        self._anything_done = True
        logger.debug("_prepar_io_handler_cb called for {0!r}".format(handler))
        self._configure_io_handler(handler)
        self._prepare_sources.pop(handler, None)
        return False