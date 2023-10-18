def sys_lseek(self, fd, offset, whence):
        """
        lseek - reposition read/write file offset

        The lseek() function repositions the file offset of the open file description associated
        with the file descriptor fd to the argument offset according to the directive whence


        :param fd: a valid file descriptor
        :param offset: the offset in bytes
        :param whence: SEEK_SET: The file offset is set to offset bytes.
                       SEEK_CUR: The file offset is set to its current location plus offset bytes.
                       SEEK_END: The file offset is set to the size of the file plus offset bytes.

        :return: offset from file beginning, or EBADF (fd is not a valid file descriptor or is not open)

        """
        signed_offset = self._to_signed_dword(offset)
        try:
            return self._get_fd(fd).seek(signed_offset, whence)
        except FdError as e:
            logger.info(("LSEEK: Not valid file descriptor on lseek."
                         "Fd not seekable. Returning EBADF"))
            return -e.err