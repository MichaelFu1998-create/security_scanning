def set_window_size(self, width, height, window_handle='current'):
        """Sets the width and height of the current window.

        Support:
            Web(WebView)

        Args:
            width(int): the width in pixels.
            height(int): the height in pixels.
            window_handle(str): Identifier of window_handle,
                default to 'current'.

        Returns:
            WebDriver Object.
        """
        self._execute(Command.SET_WINDOW_SIZE, {
            'width': int(width),
            'height': int(height),
            'window_handle': window_handle})