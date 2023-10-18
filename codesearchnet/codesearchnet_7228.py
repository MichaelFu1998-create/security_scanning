def _handle_event(self, conv_event):
        """Handle updating and scrolling when a new event is added.

        Automatically scroll down to show the new text if the bottom is
        showing. This allows the user to scroll up to read previous messages
        while new messages are arriving.
        """
        if not self._is_scrolling:
            self.set_focus(conv_event.id_)
        else:
            self._modified()