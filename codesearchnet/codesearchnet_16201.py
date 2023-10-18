def element(self, using, value):
        """Find an element in the current context.

        Support:
            Android iOS Web(WebView)

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            WebElement Object.

        Raises:
            WebDriverException.
        """
        return self._execute(Command.FIND_ELEMENT, {
            'using': using,
            'value': value
        })