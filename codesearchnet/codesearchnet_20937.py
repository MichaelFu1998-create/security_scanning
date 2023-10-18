def received(self, messages):
        """ Called when new messages arrive.

        Args:
            messages (tuple): Messages
        """
        if messages:
            if self._queue:
                self._queue.put_nowait(messages)

            if self._callback:
                self._callback(messages)