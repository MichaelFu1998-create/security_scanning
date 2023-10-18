def _queueMouseButton(self, coord, mouseButton, modFlags, clickCount=1,
                          dest_coord=None):
        """Private method to handle generic mouse button clicking.

        Parameters: coord (x, y) to click, mouseButton (e.g.,
                    kCGMouseButtonLeft), modFlags set (int)
        Optional: clickCount (default 1; set to 2 for double-click; 3 for
                  triple-click on host)
        Returns: None
        """
        # For now allow only left and right mouse buttons:
        mouseButtons = {
            Quartz.kCGMouseButtonLeft: 'LeftMouse',
            Quartz.kCGMouseButtonRight: 'RightMouse',
        }
        if mouseButton not in mouseButtons:
            raise ValueError('Mouse button given not recognized')

        eventButtonDown = getattr(Quartz,
                                  'kCGEvent%sDown' % mouseButtons[mouseButton])
        eventButtonUp = getattr(Quartz,
                                'kCGEvent%sUp' % mouseButtons[mouseButton])
        eventButtonDragged = getattr(Quartz,
                                     'kCGEvent%sDragged' % mouseButtons[
                                         mouseButton])

        # Press the button
        buttonDown = Quartz.CGEventCreateMouseEvent(None,
                                                    eventButtonDown,
                                                    coord,
                                                    mouseButton)
        # Set modflags (default None) on button down:
        Quartz.CGEventSetFlags(buttonDown, modFlags)

        # Set the click count on button down:
        Quartz.CGEventSetIntegerValueField(buttonDown,
                                           Quartz.kCGMouseEventClickState,
                                           int(clickCount))

        if dest_coord:
            # Drag and release the button
            buttonDragged = Quartz.CGEventCreateMouseEvent(None,
                                                           eventButtonDragged,
                                                           dest_coord,
                                                           mouseButton)
            # Set modflags on the button dragged:
            Quartz.CGEventSetFlags(buttonDragged, modFlags)

            buttonUp = Quartz.CGEventCreateMouseEvent(None,
                                                      eventButtonUp,
                                                      dest_coord,
                                                      mouseButton)
        else:
            # Release the button
            buttonUp = Quartz.CGEventCreateMouseEvent(None,
                                                      eventButtonUp,
                                                      coord,
                                                      mouseButton)
        # Set modflags on the button up:
        Quartz.CGEventSetFlags(buttonUp, modFlags)

        # Set the click count on button up:
        Quartz.CGEventSetIntegerValueField(buttonUp,
                                           Quartz.kCGMouseEventClickState,
                                           int(clickCount))
        # Queue the events
        self._queueEvent(Quartz.CGEventPost,
                         (Quartz.kCGSessionEventTap, buttonDown))
        if dest_coord:
            self._queueEvent(Quartz.CGEventPost,
                             (Quartz.kCGHIDEventTap, buttonDragged))
        self._queueEvent(Quartz.CGEventPost,
                         (Quartz.kCGSessionEventTap, buttonUp))