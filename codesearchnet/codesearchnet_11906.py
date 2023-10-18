def clone(self, remote_url, path=None, use_sudo=False, user=None):
        """
        Clone a remote Git repository into a new directory.

        :param remote_url: URL of the remote repository to clone.
        :type remote_url: str

        :param path: Path of the working copy directory.  Must not exist yet.
        :type path: str

        :param use_sudo: If ``True`` execute ``git`` with
                         :func:`fabric.operations.sudo`, else with
                         :func:`fabric.operations.run`.
        :type use_sudo: bool

        :param user: If ``use_sudo is True``, run :func:`fabric.operations.sudo`
                     with the given user.  If ``use_sudo is False`` this parameter
                     has no effect.
        :type user: str
        """

        cmd = 'git clone --quiet %s' % remote_url
        if path is not None:
            cmd = cmd + ' %s' % path

        if use_sudo and user is None:
            run_as_root(cmd)
        elif use_sudo:
            sudo(cmd, user=user)
        else:
            run(cmd)