def switch_to_window(self, window_name):
        """Switch to the given window.

        Support:
            Web(WebView)

        Args:
            window_name(str): The window to change focus to.

        Returns:
            WebDriver Object.
        """
        data = {
            'name': window_name
        }
        self._execute(Command.SWITCH_TO_WINDOW, data)