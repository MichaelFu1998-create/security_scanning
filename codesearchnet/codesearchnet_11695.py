def umask(self, use_sudo=False):
        """
        Get the user's umask.

        Returns a string such as ``'0002'``, representing the user's umask
        as an octal number.

        If `use_sudo` is `True`, this function returns root's umask.
        """
        func = use_sudo and run_as_root or self.run
        return func('umask')