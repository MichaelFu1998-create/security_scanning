def _is_fd_open(self, fd):
        """
        Determines if the fd is within range and in the file descr. list
        :param fd: the file descriptor to check.
        """
        return fd >= 0 and fd < len(self.files) and self.files[fd] is not None