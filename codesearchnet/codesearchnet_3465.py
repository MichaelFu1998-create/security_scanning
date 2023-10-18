def _close(self, fd):
        """
        Removes a file descriptor from the file descriptor list
        :rtype: int
        :param fd: the file descriptor to close.
        :return: C{0} on success.
        """
        try:
            self.files[fd].close()
            self._closed_files.append(self.files[fd])  # Keep track for SymbolicFile testcase generation
            self.files[fd] = None
        except IndexError:
            raise FdError(f"Bad file descriptor ({fd})")