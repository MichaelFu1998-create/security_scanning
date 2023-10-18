def init(self):
        """Create Session by desiredCapabilities

        Support:
            Android iOS Web(WebView)

        Returns:
            WebDriver Object.
        """
        resp = self._execute(Command.NEW_SESSION, {
            'desiredCapabilities': self.desired_capabilities
        }, False)
        resp.raise_for_status()
        self.session_id = str(resp.session_id)
        self.capabilities = resp.value