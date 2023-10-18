def sys_open(self, buf, flags, mode):
        """
        :param buf: address of zero-terminated pathname
        :param flags: file access bits
        :param mode: file permission mode
        """
        filename = self.current.read_string(buf)
        try:
            f = self._sys_open_get_file(filename, flags)
            logger.debug(f"Opening file {filename} for real fd {f.fileno()}")
        except IOError as e:
            logger.warning(f"Could not open file {filename}. Reason: {e!s}")
            return -e.errno if e.errno is not None else -errno.EINVAL

        return self._open(f)