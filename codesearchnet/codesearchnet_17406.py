def clickMouseButtonRightWithMods(self, coord, modifiers):
        """Click the right mouse button with modifiers pressed.

        Parameters: coordinates to click; modifiers (list)
        Returns: None
        """
        modFlags = self._pressModifiers(modifiers)
        self._queueMouseButton(coord, Quartz.kCGMouseButtonRight, modFlags)
        self._releaseModifiers(modifiers)
        self._postQueuedEvents()