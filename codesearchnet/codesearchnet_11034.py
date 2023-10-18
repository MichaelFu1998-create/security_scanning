def keyReleaseEvent(self, event):
        """
        Pyqt specific key release callback function.
        Translates and forwards events to :py:func:`keyboard_event`.
        """
        self.keyboard_event(event.key(), self.keys.ACTION_RELEASE, 0)