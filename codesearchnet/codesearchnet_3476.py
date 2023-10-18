def sys_openat(self, dirfd, buf, flags, mode):
        """
        Openat SystemCall - Similar to open system call except dirfd argument
        when path contained in buf is relative, dirfd is referred to set the relative path
        Special value AT_FDCWD set for dirfd to set path relative to current directory

        :param dirfd: directory file descriptor to refer in case of relative path at buf
        :param buf: address of zero-terminated pathname
        :param flags: file access bits
        :param mode: file permission mode
        """

        filename = self.current.read_string(buf)
        dirfd = ctypes.c_int32(dirfd).value

        if os.path.isabs(filename) or dirfd == self.FCNTL_FDCWD:
            return self.sys_open(buf, flags, mode)

        try:
            dir_entry = self._get_fd(dirfd)
        except FdError as e:
            logger.info("openat: Not valid file descriptor. Returning EBADF")
            return -e.err

        if not isinstance(dir_entry, Directory):
            logger.info("openat: Not directory descriptor. Returning ENOTDIR")
            return -errno.ENOTDIR

        dir_path = dir_entry.name

        filename = os.path.join(dir_path, filename)
        try:
            f = self._sys_open_get_file(filename, flags)
            logger.debug(f"Opening file {filename} for real fd {f.fileno()}")
        except IOError as e:
            logger.info(f"Could not open file {filename}. Reason: {e!s}")
            return -e.errno if e.errno is not None else -errno.EINVAL

        return self._open(f)