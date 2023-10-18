def _on_event(self, _):
        """Re-order the conversations when an event occurs."""
        # TODO: handle adding new conversations
        self.sort(key=lambda conv_button: conv_button.last_modified,
                  reverse=True)