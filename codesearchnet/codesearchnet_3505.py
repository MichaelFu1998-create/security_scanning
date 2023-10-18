def sys_openat(self, dirfd, buf, flags, mode):
        """
        A version of openat that includes a symbolic path and symbolic directory file descriptor

        :param dirfd: directory file descriptor
        :param buf: address of zero-terminated pathname
        :param flags: file access bits
        :param mode: file permission mode
        """

        if issymbolic(dirfd):
            logger.debug("Ask to read from a symbolic directory file descriptor!!")
            # Constrain to a valid fd and one past the end of fds
            self.constraints.add(dirfd >= 0)
            self.constraints.add(dirfd <= len(self.files))
            raise ConcretizeArgument(self, 0)

        if issymbolic(buf):
            logger.debug("Ask to read to a symbolic buffer")
            raise ConcretizeArgument(self, 1)

        return super().sys_openat(dirfd, buf, flags, mode)