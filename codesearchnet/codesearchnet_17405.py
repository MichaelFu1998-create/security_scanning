def clickMouseButtonLeftWithMods(self, coord, modifiers, interval=None):
        """Click the left mouse button with modifiers pressed.

        Parameters: coordinates to click; modifiers (list) (e.g. [SHIFT] or
                    [COMMAND, SHIFT] (assuming you've first used
                    from pyatom.AXKeyCodeConstants import *))
        Returns: None
        """
        modFlags = self._pressModifiers(modifiers)
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags)
        self._releaseModifiers(modifiers)
        if interval:
            self._postQueuedEvents(interval=interval)
        else:
            self._postQueuedEvents()