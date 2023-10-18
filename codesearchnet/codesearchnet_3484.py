def sys_close(self, fd):
        """
        Closes a file descriptor
        :rtype: int
        :param fd: the file descriptor to close.
        :return: C{0} on success.
        """
        if self._is_fd_open(fd):
            self._close(fd)
        else:
            return -errno.EBADF
        logger.debug(f'sys_close({fd})')
        return 0