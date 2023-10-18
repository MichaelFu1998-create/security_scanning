def event(self, event):
        """Pass an event to the target stream or just log it."""
        logger.debug(u"TCP transport event: {0}".format(event))
        if self._stream:
            event.stream = self._stream
        self._event_queue.put(event)