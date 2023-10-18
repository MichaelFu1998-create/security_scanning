def _input_filter(self, keys, _):
        """Handle global keybindings."""
        if keys == [self._keys['menu']]:
            if self._urwid_loop.widget == self._tabbed_window:
                self._show_menu()
            else:
                self._hide_menu()
        elif keys == [self._keys['quit']]:
            self._coroutine_queue.put(self._client.disconnect())
        else:
            return keys