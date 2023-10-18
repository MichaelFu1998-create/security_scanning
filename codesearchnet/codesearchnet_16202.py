def element_if_exists(self, using, value):
        """Check if an element in the current context.

        Support:
            Android iOS Web(WebView)

        Args:
            using(str): The element location strategy.
            value(str): The value of the location strategy.

        Returns:
            Return True if the element does exists and return False otherwise.

        Raises:
            WebDriverException.
        """
        try:
            self._execute(Command.FIND_ELEMENT, {
                'using': using,
                'value': value
            })
            return True
        except:
            return False