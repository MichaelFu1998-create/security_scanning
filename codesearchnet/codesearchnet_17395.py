def _getApplication(self):
        """Get the base application UIElement.

        If the UIElement is a child of the application, it will try
        to get the AXParent until it reaches the top application level
        element.
        """
        app = self
        while True:
            try:
                app = app.AXParent
            except _a11y.ErrorUnsupported:
                break
        return app