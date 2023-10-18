def write_string(self, where, string, max_length=None, force=False):
        """
        Writes a string to memory, appending a NULL-terminator at the end.
        :param int where: Address to write the string to
        :param str string: The string to write to memory
        :param int max_length:
            The size in bytes to cap the string at, or None [default] for no
            limit. This includes the NULL terminator.
        :param force: whether to ignore memory permissions
        """

        if max_length is not None:
            string = string[:max_length - 1]

        self.write_bytes(where, string + '\x00', force)