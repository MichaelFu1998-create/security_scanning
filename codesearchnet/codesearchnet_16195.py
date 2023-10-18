def flick(self, element, x, y, speed):
        """Deprecated use touch('drag', { fromX, fromY, toX, toY, duration(s) }) instead.
            Flick on the touch screen using finger motion events.
            This flickcommand starts at a particulat screen location.


        Support:
            iOS

        Args:
            element(WebElement): WebElement Object where the flick starts.
            x(float}: The x offset in pixels to flick by.
            y(float): The y offset in pixels to flick by.
            speed(float) The speed in pixels per seconds.

        Returns:
            WebDriver object.
        """
        self._execute(Command.FLICK, {
            'element': element.element_id,
            'x': x,
            'y': y,
            'speed': speed
        })