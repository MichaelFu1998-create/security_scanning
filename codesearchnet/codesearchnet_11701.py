def move(self, source, destination, use_sudo=False):
        """
        Move a file or directory
        """
        func = use_sudo and run_as_root or self.run
        func('/bin/mv {0} {1}'.format(quote(source), quote(destination)))