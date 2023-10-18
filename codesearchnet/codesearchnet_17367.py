def getAnyAppWithWindow(cls):
        """Get a random app that has windows.

        Raise a ValueError exception if no GUI applications are found.
        """
        # Refresh the runningApplications list
        apps = cls._getRunningApps()
        for app in apps:
            pid = app.processIdentifier()
            ref = cls.getAppRefByPid(pid)
            if hasattr(ref, 'windows') and len(ref.windows()) > 0:
                return ref
        raise ValueError('No GUI application found.')