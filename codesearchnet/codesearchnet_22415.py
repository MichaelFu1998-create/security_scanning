def send_keys(self, keys, wait=True):
        """
        Send a raw key sequence to *Vim*.

        .. note:: *Vim* style key sequence notation (like ``<Esc>``)
                  is not recognized.
                  Use escaped characters (like ``'\033'``) instead.

        Example:

        >>> import headlessvim
        >>> with headlessvim.open() as vim:
        ...     vim.send_keys('ispam\033')
        ...     str(vim.display_lines()[0].strip())
        ...
        'spam'

        :param strgin keys: key sequence to send
        :param boolean wait: whether if wait a response
        """
        self._process.stdin.write(bytearray(keys, self._encoding))
        self._process.stdin.flush()
        if wait:
            self.wait()