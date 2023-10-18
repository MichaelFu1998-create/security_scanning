def _getBundleId(self):
        """Return the bundle ID of the application."""
        ra = AppKit.NSRunningApplication
        app = ra.runningApplicationWithProcessIdentifier_(
            self._getPid())
        return app.bundleIdentifier()