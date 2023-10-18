def command(self, command, capture=True):
        """
        Execute command on *Vim*.
        .. warning:: Do not use ``redir`` command if ``capture`` is ``True``.
        It's already enabled for internal use.

        If ``capture`` argument is set ``False``,
        the command execution becomes slightly faster.

        Example:

        >>> import headlessvim
        >>> with headlessvim.open() as vim:
        ...     vim.command('echo 0')
        ...
        '0'
        >>> with headlessvim.open() as vim:
        ...     vim.command('let g:spam = "ham"', False)
        ...     vim.echo('g:spam')
        ...
        'ham'

        :param string command: a command to execute
        :param boolean capture: ``True`` if command's output needs to be
                                captured, else ``False``
        :return: the output of the given command
        :rtype: string
        """
        if capture:
            self.command('redir! >> {0}'.format(self._tempfile.name), False)
        self.set_mode('command')
        self.send_keys('{0}\n'.format(command))
        if capture:
            self.command('redir END', False)
            return self._tempfile.read().strip('\n')