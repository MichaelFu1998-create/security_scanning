def switch_to_frame(self, frame_reference=None):
        """Switches focus to the specified frame, by index, name, or webelement.

        Support:
            Web(WebView)

        Args:
            frame_reference(None|int|WebElement):
                The identifier of the frame to switch to.
                None means to set to the default context.
                An integer representing the index.
                A webelement means that is an (i)frame to switch to.
                Otherwise throw an error.

        Returns:
            WebDriver Object.
        """
        if frame_reference is not None and type(frame_reference) not in [int, WebElement]:
            raise TypeError('Type of frame_reference must be None or int or WebElement')
        self._execute(Command.SWITCH_TO_FRAME,
            {'id': frame_reference})