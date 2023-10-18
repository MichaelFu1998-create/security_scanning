def sys_fsync(self, fd):
        """
        Synchronize a file's in-core state with that on disk.
        """

        ret = 0
        try:
            self.files[fd].sync()
        except IndexError:
            ret = -errno.EBADF
        except FdError:
            ret = -errno.EINVAL

        return ret