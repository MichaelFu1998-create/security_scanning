def _on_event(self, conv_event):
        """Make users stop typing when they send a message."""
        if isinstance(conv_event, hangups.ChatMessageEvent):
            self._typing_statuses[conv_event.user_id] = (
                hangups.TYPING_TYPE_STOPPED
            )
            self._update()