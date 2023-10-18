def launchAppByBundleId(bundleID):
        """Launch the application with the specified bundle ID"""
        # NSWorkspaceLaunchAllowingClassicStartup does nothing on any
        # modern system that doesn't have the classic environment installed.
        # Encountered a bug when passing 0 for no options on 10.6 PyObjC.
        ws = AppKit.NSWorkspace.sharedWorkspace()
        # Sorry about the length of the following line
        r = ws.launchAppWithBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifier_(
            bundleID,
            AppKit.NSWorkspaceLaunchAllowingClassicStartup,
            AppKit.NSAppleEventDescriptor.nullDescriptor(),
            None)
        # On 10.6, this returns a tuple - first element bool result, second is
        # a number. Let's use the bool result.
        if not r[0]:
            raise RuntimeError('Error launching specified application.')