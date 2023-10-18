def set_window_position(self, x, y, window_handle='current'):
        """Sets the x,y position of the current window.

        Support:
            Web(WebView)

        Args:
            x(int): the x-coordinate in pixels.
            y(int): the y-coordinate in pixels.
            window_handle(str): Identifier of window_handle,
                default to 'current'.

        Returns:
            WebDriver Object.
        """
        self._execute(Command.SET_WINDOW_POSITION, {
            'x': int(x),
            'y': int(y),
            'window_handle': window_handle})