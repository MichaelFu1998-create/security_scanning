def flick(self, x, y, speed):
        """Deprecated use touch('drag', { fromX, fromY, toX, toY, duration(s) }) instead.
            Flick on the touch screen using finger motion events.
            This flickcommand starts at a particulat screen location.

        Support:
            iOS

        Args:
            x(float}: The x offset in pixels to flick by.
            y(float): The y offset in pixels to flick by.
            speed(float) The speed in pixels per seconds.

        Returns:
            WebElement object.
        """
        self._driver.flick(self, x, y, speed)