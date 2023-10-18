def last_modified(self):
        """When conversation was last modified (:class:`datetime.datetime`)."""
        timestamp = self._conversation.self_conversation_state.sort_timestamp
        # timestamp can be None for some reason when there is an ongoing video
        # hangout
        if timestamp is None:
            timestamp = 0
        return parsers.from_timestamp(timestamp)