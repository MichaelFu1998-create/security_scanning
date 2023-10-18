def _dispatch_event(self):
        """
        Dispatch the event to the handler.
        """
        data = self._prepare_data()
        if data is not None:
            self._handler(self._event, data)

        self._reset_event_data()