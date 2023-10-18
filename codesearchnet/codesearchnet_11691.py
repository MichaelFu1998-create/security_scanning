def is_file(self, path, use_sudo=False):
        """
        Check if a path exists, and is a file.
        """
        if self.is_local and not use_sudo:
            return os.path.isfile(path)
        else:
            func = use_sudo and _sudo or _run
            with self.settings(hide('running', 'warnings'), warn_only=True):
                return func('[ -f "%(path)s" ]' % locals()).succeeded