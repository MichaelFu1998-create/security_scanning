def cross_check_launchers(self, launchers):
        """
        Performs consistency checks across all the launchers.
        """
        if len(launchers) == 0: raise Exception('Empty launcher list')
        timestamps = [launcher.timestamp for launcher in launchers]

        if not all(timestamps[0] == tstamp for tstamp in timestamps):
            raise Exception("Launcher timestamps not all equal. "
                            "Consider setting timestamp explicitly.")

        root_directories = []
        for launcher in launchers:
            command = launcher.command
            args = launcher.args
            command.verify(args)
            root_directory = launcher.get_root_directory()
            if os.path.isdir(root_directory):
                raise Exception("Root directory already exists: %r" % root_directory)
            if root_directory in root_directories:
                raise Exception("Each launcher requires a unique root directory")
            root_directories.append(root_directory)