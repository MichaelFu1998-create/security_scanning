def sys_random(self, cpu, buf, count, rnd_bytes):
        """ random - fill a buffer with random data

           The  random  system call populates the buffer referenced by buf with up to
           count bytes of random data. If count is zero, random returns 0 and optionally
           sets *rx_bytes to zero. If count is greater than SSIZE_MAX, the result is unspecified.

           :param cpu: current CPU
           :param buf: a memory buffer
           :param count: max number of bytes to receive
           :param rnd_bytes: if valid, points to the actual number of random bytes

           :return:  0        On success
                     EINVAL   count is invalid.
                     EFAULT   buf or rnd_bytes points to an invalid address.
        """

        ret = 0
        if count != 0:
            if count > Decree.CGC_SSIZE_MAX or count < 0:
                ret = Decree.CGC_EINVAL
            else:
                # TODO check count bytes from buf
                if buf not in cpu.memory or (buf + count) not in cpu.memory:
                    logger.info("RANDOM: buf points to invalid address. Returning EFAULT")
                    return Decree.CGC_EFAULT

                with open("/dev/urandom", "rb") as f:
                    data = f.read(count)

                self.syscall_trace.append(("_random", -1, data))
                cpu.write_bytes(buf, data)

        # TODO check 4 bytes from rx_bytes
        if rnd_bytes:
            if rnd_bytes not in cpu.memory:
                logger.info("RANDOM: Not valid rnd_bytes. Returning EFAULT")
                return Decree.CGC_EFAULT
            cpu.write_int(rnd_bytes, len(data), 32)

        logger.info("RANDOM(0x%08x, %d, 0x%08x) -> <%s>)" % (buf, count, rnd_bytes, repr(data[:10])))
        return ret