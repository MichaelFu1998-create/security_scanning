def _set_title(self):
        """Update this conversation's tab title."""
        self.title = get_conv_name(self._conversation, show_unread=True,
                                   truncate=True)
        self._set_title_cb(self, self.title)