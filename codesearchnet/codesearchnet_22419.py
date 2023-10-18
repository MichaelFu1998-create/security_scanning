def set_mode(self, mode):
        """
        Set *Vim* mode to ``mode``.
        Supported modes:

        * ``normal``
        * ``insert``
        * ``command``
        * ``visual``
        * ``visual-block``


        This method behave as setter-only property.

        Example:

        >>> import headlessvim
        >>> with headlessvim.open() as vim:
        ...     vim.set_mode('insert')
        ...     vim.mode = 'normal' # also accessible as property
        ...

        :param string mode: *Vim* mode to set
        :raises ValueError: if ``mode`` is not supported
        """
        keys = '\033\033'
        if mode == 'normal':
            pass
        elif mode == 'insert':
            keys += 'i'
        elif mode == 'command':
            keys += ':'
        elif mode == 'visual':
            keys += 'v'
        elif mode == 'visual-block':
            keys += 'V'
        else:
            raise ValueError('mode {0} is not supported'.format(mode))
        self.send_keys(keys)