def sys_fdwait(self, cpu, nfds, readfds, writefds, timeout, readyfds):
        """ fdwait - wait for file descriptors to become ready
        """
        logger.debug("FDWAIT(%d, 0x%08x, 0x%08x, 0x%08x, 0x%08x)" % (nfds, readfds, writefds, timeout, readyfds))

        if timeout:
            if timeout not in cpu.memory:  # todo: size
                logger.info("FDWAIT: timeout is pointing to invalid memory. Returning EFAULT")
                return Decree.CGC_EFAULT

        if readyfds:
            if readyfds not in cpu.memory:
                logger.info("FDWAIT: readyfds pointing to invalid memory. Returning EFAULT")
                return Decree.CGC_EFAULT

        writefds_wait = set()
        writefds_ready = set()

        fds_bitsize = (nfds + 7) & ~7
        if writefds:
            if writefds not in cpu.memory:
                logger.info("FDWAIT: writefds pointing to invalid memory. Returning EFAULT")
                return Decree.CGC_EFAULT
            bits = cpu.read_int(writefds, fds_bitsize)

            for fd in range(nfds):
                if (bits & 1 << fd):
                    if self.files[fd].is_full():
                        writefds_wait.add(fd)
                    else:
                        writefds_ready.add(fd)

        readfds_wait = set()
        readfds_ready = set()
        if readfds:
            if readfds not in cpu.memory:
                logger.info("FDWAIT: readfds pointing to invalid memory. Returning EFAULT")
                return Decree.CGC_EFAULT
            bits = cpu.read_int(readfds, fds_bitsize)
            for fd in range(nfds):
                if (bits & 1 << fd):
                    if self.files[fd].is_empty():
                        readfds_wait.add(fd)
                    else:
                        readfds_ready.add(fd)
        n = len(readfds_ready) + len(writefds_ready)
        if n == 0:
            # TODO FIX timeout symbolic
            if timeout != 0:
                seconds = cpu.read_int(timeout, 32)
                microseconds = cpu.read_int(timeout + 4, 32)
                logger.info("FDWAIT: waiting for read on fds: {%s} and write to: {%s} timeout: %d", repr(
                    list(readfds_wait)), repr(list(writefds_wait)), microseconds + 1000 * seconds)
                to = microseconds + 1000 * seconds
                # no ready file, wait
            else:
                to = None
                logger.info("FDWAIT: waiting for read on fds: {%s} and write to: {%s} timeout: INDIFENITELY",
                            repr(list(readfds_wait)), repr(list(writefds_wait)))

            cpu.PC -= cpu.instruction.size
            self.wait(readfds_wait, writefds_wait, to)
            raise RestartSyscall()  # When coming back from a timeout remember
            # not to backtrack instruction and set EAX to 0! :( ugliness alert!

        if readfds:
            bits = 0
            for fd in readfds_ready:
                bits |= 1 << fd
            for byte in range(0, nfds, 8):
                cpu.write_int(readfds, (bits >> byte) & 0xff, 8)
        if writefds:
            bits = 0
            for fd in writefds_ready:
                bits |= 1 << fd
            for byte in range(0, nfds, 8):
                cpu.write_int(writefds, (bits >> byte) & 0xff, 8)

        logger.info("FDWAIT: continuing. Some file is ready Readyfds: %08x", readyfds)
        if readyfds:
            cpu.write_int(readyfds, n, 32)

        self.syscall_trace.append(("_fdwait", -1, None))
        return 0