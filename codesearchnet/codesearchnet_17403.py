def clickMouseButtonLeft(self, coord, interval=None):
        """Click the left mouse button without modifiers pressed.

        Parameters: coordinates to click on screen (tuple (x, y))
        Returns: None
        """

        modFlags = 0
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags)
        if interval:
            self._postQueuedEvents(interval=interval)
        else:
            self._postQueuedEvents()