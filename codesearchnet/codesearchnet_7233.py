def keypress(self, size, key):
        """Handle marking messages as read and keeping client active."""
        # Set the client as active.
        self._coroutine_queue.put(self._client.set_active())

        # Mark the newest event as read.
        self._coroutine_queue.put(self._conversation.update_read_timestamp())

        return super().keypress(size, key)