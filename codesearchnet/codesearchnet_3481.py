def sys_dup(self, fd):
        """
        Duplicates an open file descriptor
        :rtype: int
        :param fd: the open file descriptor to duplicate.
        :return: the new file descriptor.
        """

        if not self._is_fd_open(fd):
            logger.info("DUP: Passed fd is not open. Returning EBADF")
            return -errno.EBADF

        newfd = self._dup(fd)
        return newfd