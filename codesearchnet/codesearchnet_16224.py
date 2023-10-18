def move_to(self, x=0, y=0):
        """Deprecated use element.touch('drag', { toX, toY, duration(s) }) instead.
            Move the mouse by an offset of the specificed element.

        Support:
            Android

        Args:
            x(float): X offset to move to, relative to the
                      top-left corner of the element.
            y(float): Y offset to move to, relative to the
                      top-left corner of the element.

        Returns:
            WebElement object.
        """
        self._driver.move_to(self, x, y)