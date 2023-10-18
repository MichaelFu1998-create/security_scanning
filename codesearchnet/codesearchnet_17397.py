def _activate(self):
        """Activate the application (bringing menus and windows forward)."""
        ra = AppKit.NSRunningApplication
        app = ra.runningApplicationWithProcessIdentifier_(
            self._getPid())
        # NSApplicationActivateAllWindows | NSApplicationActivateIgnoringOtherApps
        # == 3 - PyObjC in 10.6 does not expose these constants though so I have
        # to use the int instead of the symbolic names
        app.activateWithOptions_(3)