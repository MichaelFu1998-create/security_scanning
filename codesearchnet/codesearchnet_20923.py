def is_text(self):
        """ Tells if this message is a text message.

        Returns:
            bool. Success
        """
        return self.type in [
            self._TYPE_PASTE,
            self._TYPE_TEXT,
            self._TYPE_TWEET
        ]