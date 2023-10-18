def sys_getcwd(self, buf, size):
        """
        getcwd - Get the current working directory
        :param int buf: Pointer to dest array
        :param size: size in bytes of the array pointed to by the buf
        :return: buf (Success), or 0
        """

        try:
            current_dir = os.getcwd()
            length = len(current_dir) + 1

            if size > 0 and size < length:
                logger.info("GETCWD: size is greater than 0, but is smaller than the length"
                            "of the path + 1. Returning ERANGE")
                return -errno.ERANGE

            if not self.current.memory.access_ok(slice(buf, buf + length), 'w'):
                logger.info("GETCWD: buf within invalid memory. Returning EFAULT")
                return -errno.EFAULT

            self.current.write_string(buf, current_dir)
            logger.debug(f"getcwd(0x{buf:08x}, {size}) -> <{current_dir}> (Size {length})")
            return length

        except OSError as e:
            return -e.errno