def unread_events(self):
        """Loaded events which are unread sorted oldest to newest.

        Some Hangouts clients don't update the read timestamp for certain event
        types, such as membership changes, so this may return more unread
        events than these clients will show. There's also a delay between
        sending a message and the user's own message being considered read.

        (list of :class:`.ConversationEvent`).
        """
        return [conv_event for conv_event in self._events
                if conv_event.timestamp > self.latest_read_timestamp]