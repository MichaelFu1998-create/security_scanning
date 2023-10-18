def elements(self, using, value):
        """Find elements in the current context.

        Support:
            Android iOS Web(WebView)

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            Return a List<Element | None>, if no element matched, the list is empty.

        Raises:
            WebDriverException.
        """
        return self._execute(Command.FIND_ELEMENTS, {
            'using': using,
            'value': value
        })