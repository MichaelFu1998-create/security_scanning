def copy(self, source, destination, recursive=False, use_sudo=False):
        """
        Copy a file or directory
        """
        func = use_sudo and run_as_root or self.run
        options = '-r ' if recursive else ''
        func('/bin/cp {0}{1} {2}'.format(options, quote(source), quote(destination)))