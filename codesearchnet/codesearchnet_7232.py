def get_menu_widget(self, close_callback):
        """Return the menu widget associated with this widget."""
        return ConversationMenu(
            self._coroutine_queue, self._conversation, close_callback,
            self._keys
        )