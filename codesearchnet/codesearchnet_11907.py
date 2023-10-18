def add_remote(self, path, name, remote_url, use_sudo=False, user=None, fetch=True):
        """
        Add a remote Git repository into a directory.

        :param path: Path of the working copy directory.  This directory must exist
                     and be a Git working copy with a default remote to fetch from.
        :type path: str

        :param use_sudo: If ``True`` execute ``git`` with
                         :func:`fabric.operations.sudo`, else with
                         :func:`fabric.operations.run`.
        :type use_sudo: bool

        :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                     with the given user.  If ``use_sudo is False`` this parameter
                     has no effect.
        :type user: str

        :param name: name for the remote repository
        :type name: str

        :param remote_url: URL of the remote repository
        :type remote_url: str

        :param fetch: If ``True`` execute ``git remote add -f``
        :type fetch: bool
        """
        if path is None:
            raise ValueError("Path to the working copy is needed to add a remote")

        if fetch:
            cmd = 'git remote add -f %s %s' % (name, remote_url)
        else:
            cmd = 'git remote add %s %s' % (name, remote_url)

        with cd(path):
            if use_sudo and user is None:
                run_as_root(cmd)
            elif use_sudo:
                sudo(cmd, user=user)
            else:
                run(cmd)