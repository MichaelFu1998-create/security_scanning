def show_message(self, message_str):
        """Show a temporary message."""
        if self._message_handle is not None:
            self._message_handle.cancel()
        self._message_handle = asyncio.get_event_loop().call_later(
            self._MESSAGE_DELAY_SECS, self._clear_message
        )
        self._message = message_str
        self._update()