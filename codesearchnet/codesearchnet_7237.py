def keypress(self, size, key):
        """Handle keypresses for changing tabs."""
        key = super().keypress(size, key)
        num_tabs = len(self._widgets)
        if key == self._keys['prev_tab']:
            self._tab_index = (self._tab_index - 1) % num_tabs
            self._update_tabs()
        elif key == self._keys['next_tab']:
            self._tab_index = (self._tab_index + 1) % num_tabs
            self._update_tabs()
        elif key == self._keys['close_tab']:
            # Don't allow closing the Conversations tab
            if self._tab_index > 0:
                curr_tab = self._widgets[self._tab_index]
                self._widgets.remove(curr_tab)
                del self._widget_title[curr_tab]
                self._tab_index -= 1
                self._update_tabs()
        else:
            return key