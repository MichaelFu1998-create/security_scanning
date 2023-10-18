def sys_getrandom(self, buf, size, flags):
        """
        The getrandom system call fills the buffer with random bytes of buflen.
        The source of random (/dev/random or /dev/urandom) is decided based on the flags value.

        :param buf: address of buffer to be filled with random bytes
        :param size: number of random bytes
        :param flags: source of random (/dev/random or /dev/urandom)
        :return: number of bytes copied to buf
        """

        if issymbolic(buf):
            logger.debug("sys_getrandom: Asked to generate random to a symbolic buffer address")
            raise ConcretizeArgument(self, 0)

        if issymbolic(size):
            logger.debug("sys_getrandom: Asked to generate random of symbolic number of bytes")
            raise ConcretizeArgument(self, 1)

        if issymbolic(flags):
            logger.debug("sys_getrandom: Passed symbolic flags")
            raise ConcretizeArgument(self, 2)

        return super().sys_getrandom(buf, size, flags)