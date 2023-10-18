def sys_dup2(self, fd, newfd):
        """
        Duplicates an open fd to newfd. If newfd is open, it is first closed
        :rtype: int
        :param fd: the open file descriptor to duplicate.
        :param newfd: the file descriptor to alias the file described by fd.
        :return: newfd.
        """
        try:
            file = self._get_fd(fd)
        except FdError as e:
            logger.info("DUP2: Passed fd is not open. Returning EBADF")
            return -e.err

        soft_max, hard_max = self._rlimits[self.RLIMIT_NOFILE]
        if newfd >= soft_max:
            logger.info("DUP2: newfd is above max descriptor table size")
            return -errno.EBADF

        if self._is_fd_open(newfd):
            self._close(newfd)

        if newfd >= len(self.files):
            self.files.extend([None] * (newfd + 1 - len(self.files)))

        self.files[newfd] = self.files[fd]

        logger.debug('sys_dup2(%d,%d) -> %d', fd, newfd, newfd)
        return newfd