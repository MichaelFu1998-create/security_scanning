def sys_write(self, fd, buf, count):
        """ write - send bytes through a file descriptor
          The write system call writes up to count bytes from the buffer pointed
          to by buf to the file descriptor fd. If count is zero, write returns 0
          and optionally sets *tx_bytes to zero.

          :param fd            a valid file descriptor
          :param buf           a memory buffer
          :param count         number of bytes to send
          :return: 0          Success
                    EBADF      fd is not a valid file descriptor or is not open.
                    EFAULT     buf or tx_bytes points to an invalid address.
        """
        data: bytes = bytes()
        cpu = self.current
        if count != 0:
            try:
                write_fd = self._get_fd(fd)
            except FdError as e:
                logger.error(f"WRITE: Not valid file descriptor ({fd}). Returning -{e.err}")
                return -e.err

            # TODO check count bytes from buf
            if buf not in cpu.memory or buf + count not in cpu.memory:
                logger.debug("WRITE: buf points to invalid address. Returning EFAULT")
                return -errno.EFAULT

            if fd > 2 and write_fd.is_full():
                cpu.PC -= cpu.instruction.size
                self.wait([], [fd], None)
                raise RestartSyscall()

            data: MixedSymbolicBuffer = cpu.read_bytes(buf, count)
            data: bytes = self._transform_write_data(data)
            write_fd.write(data)

            for line in data.split(b'\n'):
                line = line.decode('latin-1')  # latin-1 encoding will happily decode any byte (0x00-0xff)
                logger.debug(f"WRITE({fd}, 0x{buf:08x}, {count}) -> <{repr(line):48s}>")
            self.syscall_trace.append(("_write", fd, data))
            self.signal_transmit(fd)

        return len(data)