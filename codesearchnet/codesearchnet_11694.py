def get_owner(self, path, use_sudo=False):
        """
        Get the owner name of a file or directory.
        """
        func = use_sudo and run_as_root or self.run
        # I'd prefer to use quiet=True, but that's not supported with older
        # versions of Fabric.
        with self.settings(hide('running', 'stdout'), warn_only=True):
            result = func('stat -c %%U "%(path)s"' % locals())
            if result.failed and 'stat: illegal option' in result:
                # Try the BSD version of stat
                return func('stat -f %%Su "%(path)s"' % locals())
            return result