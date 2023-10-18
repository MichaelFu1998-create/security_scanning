def getFrontmostApp(cls):
        """Get the current frontmost application.

        Raise a ValueError exception if no GUI applications are found.
        """
        # Refresh the runningApplications list
        apps = cls._getRunningApps()
        for app in apps:
            pid = app.processIdentifier()
            ref = cls.getAppRefByPid(pid)
            try:
                if ref.AXFrontmost:
                    return ref
            except (_a11y.ErrorUnsupported,
                    _a11y.ErrorCannotComplete,
                    _a11y.ErrorAPIDisabled,
                    _a11y.ErrorNotImplemented):
                # Some applications do not have an explicit GUI
                # and so will not have an AXFrontmost attribute
                # Trying to read attributes from Google Chrome Helper returns
                # ErrorAPIDisabled for some reason - opened radar bug 12837995
                pass
        raise ValueError('No GUI application found.')