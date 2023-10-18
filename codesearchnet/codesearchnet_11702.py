def remove(self, path, recursive=False, use_sudo=False):
        """
        Remove a file or directory
        """
        func = use_sudo and run_as_root or self.run
        options = '-r ' if recursive else ''
        func('/bin/rm {0}{1}'.format(options, quote(path)))