def tripleClickMouse(self, coord):
        """Triple-click primary mouse button.

        Parameters: coordinates to click (assume primary is left button)
        Returns: None
        """
        # Note above re: double-clicks applies to triple-clicks
        modFlags = 0
        for i in range(2):
            self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags)
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags,
                               clickCount=3)
        self._postQueuedEvents()