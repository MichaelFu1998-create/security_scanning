def sys_receive(self, cpu, fd, buf, count, rx_bytes):
        """ receive - receive bytes from a file descriptor

            The receive system call reads up to count bytes from file descriptor fd to the
            buffer pointed to by buf. If count is zero, receive returns 0 and optionally
            sets *rx_bytes to zero.

            :param cpu: current CPU.
            :param fd: a valid file descriptor
            :param buf: a memory buffer
            :param count: max number of bytes to receive
            :param rx_bytes: if valid, points to the actual number of bytes received
            :return: 0            Success
                     EBADF        fd is not a valid file descriptor or is not open
                     EFAULT       buf or rx_bytes points to an invalid address.
        """
        data = ''
        if count != 0:
            if not self._is_open(fd):
                logger.info("RECEIVE: Not valid file descriptor on receive. Returning EBADF")
                return Decree.CGC_EBADF

            # TODO check count bytes from buf
            if buf not in cpu.memory:  # or not  buf+count in cpu.memory:
                logger.info("RECEIVE: buf points to invalid address. Returning EFAULT")
                return Decree.CGC_EFAULT

            #import random
            #count = random.randint(1,count)
            if fd > 2 and self.files[fd].is_empty():
                cpu.PC -= cpu.instruction.size
                self.wait([fd], [], None)
                raise RestartSyscall()

            # get some potential delay
            # if random.randint(5) == 0 and count > 1:
            #    count = count/2

            # Read the data and put it in memory
            data = self.files[fd].receive(count)
            self.syscall_trace.append(("_receive", fd, data))
            cpu.write_bytes(buf, data)

            self.signal_receive(fd)

        # TODO check 4 bytes from rx_bytes
        if rx_bytes:
            if rx_bytes not in cpu.memory:
                logger.info("RECEIVE: Not valid file descriptor on receive. Returning EFAULT")
                return Decree.CGC_EFAULT
            cpu.write_int(rx_bytes, len(data), 32)

        logger.info("RECEIVE(%d, 0x%08x, %d, 0x%08x) -> <%s> (size:%d)" % (fd, buf, count, rx_bytes, repr(data)[:min(count, 10)], len(data)))
        return 0