def keyPressEvent(self, event):
        """
        Pyqt specific key press callback function.
        Translates and forwards events to :py:func:`keyboard_event`.
        """
        self.keyboard_event(event.key(), self.keys.ACTION_PRESS, 0)