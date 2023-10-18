def _performAction(self, action):
        """Perform the specified action."""
        try:
            _a11y.AXUIElement._performAction(self, 'AX%s' % action)
        except _a11y.ErrorUnsupported as e:
            sierra_ver = '10.12'
            if mac_ver()[0] < sierra_ver:
                raise e
            else:
                pass