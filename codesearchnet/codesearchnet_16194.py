def move_to(self, element, x=0, y=0):
        """Deprecated use element.touch('drag', { toX, toY, duration(s) }) instead.
            Move the mouse by an offset of the specificed element.

        Support:
            Android

        Args:
            element(WebElement): WebElement Object.
            x(float): X offset to move to, relative to the
                      top-left corner of the element.
            y(float): Y offset to move to, relative to the
                      top-left corner of the element.

        Returns:
            WebDriver object.
        """
        self._execute(Command.MOVE_TO, {
            'element': element.element_id,
            'x': x,
            'y': y
        })