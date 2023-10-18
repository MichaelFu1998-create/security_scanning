def _leftMouseDragged(self, stopCoord, strCoord, speed):
        """Private method to handle generic mouse left button dragging and
        dropping.

        Parameters: stopCoord(x,y) drop point
        Optional: strCoord (x, y) drag point, default (0,0) get current
                  mouse position
                  speed (int) 1 to unlimit, simulate mouse moving
                  action from some special requirement
        Returns: None
        """
        # To direct output to the correct application need the PSN:
        appPid = self._getPid()
        # Get current position as start point if strCoord not given
        if strCoord == (0, 0):
            loc = AppKit.NSEvent.mouseLocation()
            strCoord = (loc.x, Quartz.CGDisplayPixelsHigh(0) - loc.y)

        # To direct output to the correct application need the PSN:
        appPid = self._getPid()

        # Press left button down
        pressLeftButton = Quartz.CGEventCreateMouseEvent(
            None,
            Quartz.kCGEventLeftMouseDown,
            strCoord,
            Quartz.kCGMouseButtonLeft
        )
        # Queue the events
        Quartz.CGEventPost(Quartz.CoreGraphics.kCGHIDEventTap, pressLeftButton)
        # Wait for reponse of system, a fuzzy icon appears
        time.sleep(5)
        # Simulate mouse moving speed, k is slope
        speed = round(1 / float(speed), 2)
        xmoved = stopCoord[0] - strCoord[0]
        ymoved = stopCoord[1] - strCoord[1]
        if ymoved == 0:
            raise ValueError('Not support horizontal moving')
        else:
            k = abs(ymoved / xmoved)

        if xmoved != 0:
            for xpos in range(int(abs(xmoved))):
                if xmoved > 0 and ymoved > 0:
                    currcoord = (strCoord[0] + xpos, strCoord[1] + xpos * k)
                elif xmoved > 0 and ymoved < 0:
                    currcoord = (strCoord[0] + xpos, strCoord[1] - xpos * k)
                elif xmoved < 0 and ymoved < 0:
                    currcoord = (strCoord[0] - xpos, strCoord[1] - xpos * k)
                elif xmoved < 0 and ymoved > 0:
                    currcoord = (strCoord[0] - xpos, strCoord[1] + xpos * k)
                # Drag with left button
                dragLeftButton = Quartz.CGEventCreateMouseEvent(
                    None,
                    Quartz.kCGEventLeftMouseDragged,
                    currcoord,
                    Quartz.kCGMouseButtonLeft
                )
                Quartz.CGEventPost(Quartz.CoreGraphics.kCGHIDEventTap,
                                   dragLeftButton)
                # Wait for reponse of system
                time.sleep(speed)
        else:
            raise ValueError('Not support vertical moving')
        upLeftButton = Quartz.CGEventCreateMouseEvent(
            None,
            Quartz.kCGEventLeftMouseUp,
            stopCoord,
            Quartz.kCGMouseButtonLeft
        )
        # Wait for reponse of system, a plus icon appears
        time.sleep(5)
        # Up left button up
        Quartz.CGEventPost(Quartz.CoreGraphics.kCGHIDEventTap, upLeftButton)