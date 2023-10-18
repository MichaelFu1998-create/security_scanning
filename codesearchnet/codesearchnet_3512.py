def sys_transmit(self, cpu, fd, buf, count, tx_bytes):
        """ transmit - send bytes through a file descriptor
          The  transmit system call writes up to count bytes from the buffer pointed
          to by buf to the file descriptor fd. If count is zero, transmit returns 0
          and optionally sets *tx_bytes to zero.

          :param cpu           current CPU
          :param fd            a valid file descriptor
          :param buf           a memory buffer
          :param count         number of bytes to send
          :param tx_bytes      if valid, points to the actual number of bytes transmitted
          :return: 0            Success
                   EBADF        fd is not a valid file descriptor or is not open.
                   EFAULT       buf or tx_bytes points to an invalid address.
        """
        data = []
        if count != 0:

            if not self._is_open(fd):
                logger.error("TRANSMIT: Not valid file descriptor. Returning EBADFD %d", fd)
                return Decree.CGC_EBADF

            # TODO check count bytes from buf
            if buf not in cpu.memory or (buf + count) not in cpu.memory:
                logger.debug("TRANSMIT: buf points to invalid address. Rerurning EFAULT")
                return Decree.CGC_EFAULT

            if fd > 2 and self.files[fd].is_full():
                cpu.PC -= cpu.instruction.size
                self.wait([], [fd], None)
                raise RestartSyscall()

            for i in range(0, count):
                value = Operators.CHR(cpu.read_int(buf + i, 8))
                if not isinstance(value, str):
                    logger.debug("TRANSMIT: Writing symbolic values to file %d", fd)
                    #value = str(value)
                data.append(value)
            self.files[fd].transmit(data)

            logger.info("TRANSMIT(%d, 0x%08x, %d, 0x%08x) -> <%.24r>" % (fd, buf, count, tx_bytes, ''.join([str(x) for x in data])))
            self.syscall_trace.append(("_transmit", fd, data))
            self.signal_transmit(fd)

        # TODO check 4 bytes from tx_bytes
        if tx_bytes:
            if tx_bytes not in cpu.memory:
                logger.debug("TRANSMIT: Not valid tx_bytes pointer on transmit. Returning EFAULT")
                return Decree.CGC_EFAULT
            cpu.write_int(tx_bytes, len(data), 32)

        return 0