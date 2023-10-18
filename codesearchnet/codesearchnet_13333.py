def _prepare_pending(self):
        """Prepare pending handlers.
        """
        if not self._unprepared_pending:
            return
        for handler in list(self._unprepared_pending):
            self._configure_io_handler(handler)
        self.check_events()