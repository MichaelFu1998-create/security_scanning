def is_link(self, path, use_sudo=False):
        """
        Check if a path exists, and is a symbolic link.
        """
        func = use_sudo and _sudo or _run
        with self.settings(hide('running', 'warnings'), warn_only=True):
            return func('[ -L "%(path)s" ]' % locals()).succeeded