def fetch(self, path, use_sudo=False, user=None, remote=None):
        """
        Fetch changes from the default remote repository.

        This will fetch new changesets, but will not update the contents of
        the working tree unless yo do a merge or rebase.

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

        :type remote: Fetch this remote or default remote if is None
        :type remote: str
        """

        if path is None:
            raise ValueError("Path to the working copy is needed to fetch from a remote repository.")

        if remote is not None:
            cmd = 'git fetch %s' % remote
        else:
            cmd = 'git fetch'

        with cd(path):
            if use_sudo and user is None:
                run_as_root(cmd)
            elif use_sudo:
                sudo(cmd, user=user)
            else:
                run(cmd)