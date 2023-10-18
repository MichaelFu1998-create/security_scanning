def notify(self, event_id):
        """Let the FlowControl system know that there is an event."""
        self._event_buffer.extend([event_id])
        self._event_count += 1
        if self._event_count >= self.threshold:
            logger.debug("Eventcount >= threshold")
            self.make_callback(kind="event")