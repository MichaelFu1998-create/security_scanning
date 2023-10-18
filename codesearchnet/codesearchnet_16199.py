def add_cookie(self, cookie_dict):
        """Set a cookie.

        Support:
            Web(WebView)

        Args:
            cookie_dict: A dictionary contain keys: "name", "value",
                ["path"], ["domain"], ["secure"], ["httpOnly"], ["expiry"].

        Returns:
            WebElement Object.
        """
        if not isinstance(cookie_dict, dict):
            raise TypeError('Type of the cookie must be a dict.')
        if not cookie_dict.get(
            'name', None
        ) or not cookie_dict.get(
            'value', None):
            raise KeyError('Missing required keys, \'name\' and \'value\' must be provided.')
        self._execute(Command.ADD_COOKIE, {'cookie': cookie_dict})