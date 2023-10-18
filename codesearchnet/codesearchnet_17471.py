def generatemouseevent(self, x, y, eventType="b1c",
                           drag_button_override='drag_default_button'):
        """
        Generate mouse event on x, y co-ordinates.
        
        @param x: X co-ordinate
        @type x: int
        @param y: Y co-ordinate
        @type y: int
        @param eventType: Mouse click type
        @type eventType: str
        @param drag_button_override: Any drag_xxx value
                Only relevant for movements, i.e. |type| = "abs" or "rel"
                Quartz is not fully compatible with windows, so for drags
                the drag button must be explicitly defined. generatemouseevent
                will remember the last button pressed by default, and drag
                that button, use this argument to override that.
        @type drag_button_override: str

        @return: 1 on success.
        @rtype: integer
        """
        if drag_button_override not in mouse_click_override:
            raise ValueError('Unsupported drag_button_override type: %s' % \
                             drag_button_override)
        global drag_button_remembered
        point = (x, y)
        button = centre  # Only matters for "other" buttons
        click_type = None
        if eventType == "abs" or eventType == "rel":
            if drag_button_override is not 'drag_default_button':
                events = [mouse_click_override[drag_button_override]]
            elif drag_button_remembered:
                events = [drag_button_remembered]
            else:
                events = [move]
            if eventType == "rel":
                point = CGEventGetLocation(CGEventCreate(None))
                point.x += x
                point.y += y
        elif eventType == "b1p":
            events = [press_left]
            drag_button_remembered = drag_left
        elif eventType == "b1r":
            events = [release_left]
            drag_button_remembered = None
        elif eventType == "b1c":
            events = [press_left, release_left]
        elif eventType == "b1d":
            events = [press_left, release_left]
            click_type = double_click
        elif eventType == "b2p":
            events = [press_other]
            drag_button_remembered = drag_other
        elif eventType == "b2r":
            events = [release_other]
            drag_button_remembered = None
        elif eventType == "b2c":
            events = [press_other, release_other]
        elif eventType == "b2d":
            events = [press_other, release_other]
            click_type = double_click
        elif eventType == "b3p":
            events = [press_right]
            drag_button_remembered = drag_right
        elif eventType == "b3r":
            events = [release_right]
            drag_button_remembered = None
        elif eventType == "b3c":
            events = [press_right, release_right]
        elif eventType == "b3d":
            events = [press_right, release_right]
            click_type = double_click
        else:
            raise LdtpServerException(u"Mouse event '%s' not implemented" % eventType)

        for event in events:
            CG_event = CGEventCreateMouseEvent(None, event, point, button)
            if click_type:
                CGEventSetIntegerValueField(
                    CG_event, kCGMouseEventClickState, click_type)
            CGEventPost(kCGHIDEventTap, CG_event)
            # Give the event time to happen
            time.sleep(0.01)
        return 1