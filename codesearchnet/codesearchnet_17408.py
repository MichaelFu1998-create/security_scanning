def doubleClickMouse(self, coord):
        """Double-click primary mouse button.

        Parameters: coordinates to click (assume primary is left button)
        Returns: None
        """
        modFlags = 0
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags)
        # This is a kludge:
        # If directed towards a Fusion VM the clickCount gets ignored and this
        # will be seen as a single click, so in sequence this will be a double-
        # click
        # Otherwise to a host app only this second one will count as a double-
        # click
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags,
                               clickCount=2)
        self._postQueuedEvents()