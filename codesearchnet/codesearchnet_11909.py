def pull(self, path, use_sudo=False, user=None, force=False):
        """
        Fetch changes from the default remote repository and merge them.

        :param path: Path of the working copy directory.  This directory must exist
                     and be a Git working copy with a default remote to pull from.
        :type path: str

        :param use_sudo: If ``True`` execute ``git`` with
                         :func:`fabric.operations.sudo`, else with
                         :func:`fabric.operations.run`.
        :type use_sudo: bool

        :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                     with the given user.  If ``use_sudo is False`` this parameter
                     has no effect.
        :type user: str
        :param force: If ``True``, append the ``--force`` option to the command.
        :type force: bool
        """

        if path is None:
            raise ValueError("Path to the working copy is needed to pull from a remote repository.")

        options = []
        if force:
            options.append('--force')
        options = ' '.join(options)

        cmd = 'git pull %s' % options

        with cd(path):
            if use_sudo and user is None:
                run_as_root(cmd)
            elif use_sudo:
                sudo(cmd, user=user)
            else:
                run(cmd)