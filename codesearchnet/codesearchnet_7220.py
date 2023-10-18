def _rename(self, name, callback):
        """Rename conversation and call callback."""
        self._coroutine_queue.put(self._conversation.rename(name))
        callback()