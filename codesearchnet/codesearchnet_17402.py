def doubleClickDragMouseButtonLeft(self, coord, dest_coord, interval=0.5):
        """Double-click and drag the left mouse button without modifiers
        pressed.

        Parameters: coordinates to double-click on screen (tuple (x, y))
                    dest coordinates to drag to (tuple (x, y))
                    interval to send event of btn down, drag and up
        Returns: None
        """
        modFlags = 0
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags,
                               dest_coord=dest_coord)
        self._queueMouseButton(coord, Quartz.kCGMouseButtonLeft, modFlags,
                               dest_coord=dest_coord,
                               clickCount=2)
        self._postQueuedEvents(interval=interval)