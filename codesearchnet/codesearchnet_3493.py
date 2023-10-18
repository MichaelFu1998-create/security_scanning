def sys_getrandom(self, buf, size, flags):
        """
        The getrandom system call fills the buffer with random bytes of buflen.
        The source of random (/dev/random or /dev/urandom) is decided based on
        the flags value.

        Manticore's implementation simply fills a buffer with zeroes -- choosing
        determinism over true randomness.

        :param buf: address of buffer to be filled with random bytes
        :param size: number of random bytes
        :param flags: source of random (/dev/random or /dev/urandom)
        :return: number of bytes copied to buf
        """

        GRND_NONBLOCK = 0x0001
        GRND_RANDOM = 0x0002

        if size == 0:
            return 0

        if buf not in self.current.memory:
            logger.info("getrandom: Provided an invalid address. Returning EFAULT")
            return -errno.EFAULT

        if flags & ~(GRND_NONBLOCK | GRND_RANDOM):
            return -errno.EINVAL

        self.current.write_bytes(buf, '\x00' * size)

        return size