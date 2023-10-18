def sys_readlink(self, path, buf, bufsize):
        """
        Read
        :rtype: int

        :param path: the "link path id"
        :param buf: the buffer where the bytes will be putted.
        :param bufsize: the max size for read the link.
        :todo: Out eax number of bytes actually sent | EAGAIN | EBADF | EFAULT | EINTR | errno.EINVAL | EIO | ENOSPC | EPIPE
        """
        if bufsize <= 0:
            return -errno.EINVAL
        filename = self.current.read_string(path)
        if filename == '/proc/self/exe':
            data = os.path.abspath(self.program)
        else:
            data = os.readlink(filename)[:bufsize]
        self.current.write_bytes(buf, data)
        return len(data)