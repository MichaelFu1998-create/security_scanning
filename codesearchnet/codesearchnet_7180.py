def next_event(self, event_id, prev=False):
        """Get the event following another event in this conversation.

        Args:
            event_id (str): ID of the event.
            prev (bool): If ``True``, return the previous event rather than the
                next event. Defaults to ``False``.

        Raises:
            KeyError: If no such :class:`.ConversationEvent` is known.

        Returns:
            :class:`.ConversationEvent` or ``None`` if there is no following
            event.
        """
        i = self.events.index(self._events_dict[event_id])
        if prev and i > 0:
            return self.events[i - 1]
        elif not prev and i + 1 < len(self.events):
            return self.events[i + 1]
        else:
            return None