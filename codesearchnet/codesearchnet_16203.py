def element_or_none(self, using, value):
        """Check if an element in the current context.

        Support:
            Android iOS Web(WebView)

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            Return Element if the element does exists and return None otherwise.

        Raises:
            WebDriverException.
        """
        try:
            return self._execute(Command.FIND_ELEMENT, {
                'using': using,
                'value': value
            })
        except:
            return None