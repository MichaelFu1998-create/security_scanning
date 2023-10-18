def set_focus(self, position):
        """Set the focus to position or raise IndexError."""
        self._focus_position = position
        self._modified()
        # If we set focus to anywhere but the last position, the user if
        # scrolling up:
        try:
            self.next_position(position)
        except IndexError:
            self._is_scrolling = False
        else:
            self._is_scrolling = True