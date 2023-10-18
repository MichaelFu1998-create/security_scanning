def launchAppByBundlePath(bundlePath, arguments=None):
        """Launch app with a given bundle path.

        Return True if succeed.
        """
        if arguments is None:
            arguments = []

        bundleUrl = NSURL.fileURLWithPath_(bundlePath)
        workspace = AppKit.NSWorkspace.sharedWorkspace()
        arguments_strings = list(map(lambda a: NSString.stringWithString_(str(a)),
                                arguments))
        arguments = NSDictionary.dictionaryWithDictionary_({
            AppKit.NSWorkspaceLaunchConfigurationArguments: NSArray.arrayWithArray_(
                arguments_strings)
        })

        return workspace.launchApplicationAtURL_options_configuration_error_(
            bundleUrl,
            AppKit.NSWorkspaceLaunchAllowingClassicStartup,
            arguments,
            None)