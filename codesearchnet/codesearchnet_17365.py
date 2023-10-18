def _getRunningApps(cls):
        """Get a list of the running applications."""

        def runLoopAndExit():
            AppHelper.stopEventLoop()

        AppHelper.callLater(1, runLoopAndExit)
        AppHelper.runConsoleEventLoop()
        # Get a list of running applications
        ws = AppKit.NSWorkspace.sharedWorkspace()
        apps = ws.runningApplications()
        return apps