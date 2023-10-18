def sys_writev(self, fd, iov, count):
        """
        Works just like C{sys_write} except that multiple buffers are written out.
        :rtype: int

        :param fd: the file descriptor of the file to write.
        :param iov: the buffer where the the bytes to write are taken.
        :param count: amount of C{iov} buffers to write into the file.
        :return: the amount of bytes written in total.
        """
        cpu = self.current
        ptrsize = cpu.address_bit_size
        sizeof_iovec = 2 * (ptrsize // 8)
        total = 0
        try:
            write_fd = self._get_fd(fd)
        except FdError as e:
            logger.error(f"writev: Not a valid file descriptor ({fd})")
            return -e.err

        for i in range(0, count):
            buf = cpu.read_int(iov + i * sizeof_iovec, ptrsize)
            size = cpu.read_int(iov + i * sizeof_iovec + (sizeof_iovec // 2), ptrsize)

            data = [Operators.CHR(cpu.read_int(buf + i, 8)) for i in range(size)]
            data = self._transform_write_data(data)
            write_fd.write(data)
            self.syscall_trace.append(("_write", fd, data))
            total += size
        return total