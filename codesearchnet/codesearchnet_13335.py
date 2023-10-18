def _remove_io_handler(self, handler):
        """Remove an i/o-handler."""
        if handler in self._unprepared_handlers:
            del self._unprepared_handlers[handler]
        tag = self._prepare_sources.pop(handler, None)
        if tag is not None:
            glib.source_remove(tag)
        tag = self._io_sources.pop(handler, None)
        if tag is not None:
            glib.source_remove(tag)