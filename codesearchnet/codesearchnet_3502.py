def sys_fstat64(self, fd, buf):
        """
        Determines information about a file based on its file descriptor (for Linux 64 bits).
        :rtype: int
        :param fd: the file descriptor of the file that is being inquired.
        :param buf: a buffer where data about the file will be stored.
        :return: C{0} on success, EBADF when called with bad fd
        :todo: Fix device number.
        """

        try:
            stat = self._get_fd(fd).stat()
        except FdError as e:
            logger.info("Calling fstat with invalid fd, returning EBADF")
            return -e.err

        def add(width, val):
            fformat = {2: 'H', 4: 'L', 8: 'Q'}[width]
            return struct.pack('<' + fformat, val)

        def to_timespec(ts):
            return struct.pack('<LL', int(ts), int(ts % 1 * 1e9))

        bufstat = add(8, stat.st_dev)        # unsigned long long      st_dev;
        bufstat += add(8, stat.st_ino)        # unsigned long long   __st_ino;
        bufstat += add(4, stat.st_mode)       # unsigned int    st_mode;
        bufstat += add(4, stat.st_nlink)      # unsigned int    st_nlink;
        bufstat += add(4, stat.st_uid)        # unsigned long   st_uid;
        bufstat += add(4, stat.st_gid)        # unsigned long   st_gid;
        bufstat += add(8, stat.st_rdev)       # unsigned long long st_rdev;
        bufstat += add(8, 0)                  # unsigned long long __pad1;
        bufstat += add(8, stat.st_size)       # long long       st_size;
        bufstat += add(4, stat.st_blksize)    # int   st_blksize;
        bufstat += add(4, 0)                  # int   __pad2;
        bufstat += add(8, stat.st_blocks)     # unsigned long long st_blocks;
        bufstat += to_timespec(stat.st_atime)  # unsigned long   st_atime;
        bufstat += to_timespec(stat.st_mtime)  # unsigned long   st_mtime;
        bufstat += to_timespec(stat.st_ctime)  # unsigned long   st_ctime;
        bufstat += add(4, 0)                   # unsigned int __unused4;
        bufstat += add(4, 0)                   # unsigned int __unused5;

        self.current.write_bytes(buf, bufstat)
        return 0