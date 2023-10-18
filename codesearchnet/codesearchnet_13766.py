def write(self, text, newline=False):
        """Use ``\\r`` to overdraw the current line with the given text.

        This function transparently handles tracking how much overdrawing is
        necessary to erase the previous line when used consistently.

        :param text: The text to be outputted
        :param newline: Whether to start a new line and reset the length count.
        :type text: :class:`~__builtins__.str`
        :type newline: :class:`~__builtins__.bool`
        """
        if not self.isatty:
            self.fobj.write('%s\n' % text)
            return

        msg_len = len(text)
        self.max_len = max(self.max_len, msg_len)

        self.fobj.write("\r%-*s" % (self.max_len, text))
        if newline or not self.isatty:
            self.fobj.write('\n')
            self.max_len = 0