def _process_events(self, events):
        """Process events from proactor."""
        for f, callback, transferred, key, ov in events:
            try:
                self._logger.debug('Invoking event callback {}'.format(callback))
                value = callback(transferred, key, ov)
            except OSError:
                self._logger.warning('Event callback failed', exc_info=sys.exc_info())
            else:
                f.set_result(value)