def terminateAppByBundleId(bundleID):
        """Terminate app with a given bundle ID.
        Requires 10.6.

        Return True if succeed.
        """
        ra = AppKit.NSRunningApplication
        if getattr(ra, "runningApplicationsWithBundleIdentifier_"):
            appList = ra.runningApplicationsWithBundleIdentifier_(bundleID)
            if appList and len(appList) > 0:
                app = appList[0]
                return app and app.terminate() and True or False
        return False