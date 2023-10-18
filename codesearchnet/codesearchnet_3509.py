def sys_allocate(self, cpu, length, isX, addr):
        """ allocate - allocate virtual memory

           The  allocate  system call creates a new allocation in the virtual address
           space of the calling process.  The length argument specifies the length of
           the allocation in bytes which will be rounded up to the hardware page size.

           The kernel chooses the address at which to create the allocation; the
           address of the new allocation is returned in *addr as the result of the call.

           All newly allocated memory is readable and writeable. In addition, the
           is_X argument is a boolean that allows newly allocated memory to be marked
           as executable (non-zero) or non-executable (zero).

           The allocate function is invoked through system call number 5.

           :param cpu: current CPU
           :param length: the length of the allocation in bytes
           :param isX: boolean that allows newly allocated memory to be marked as executable
           :param addr: the address of the new allocation is returned in *addr

           :return: On success, allocate returns zero and a pointer to the allocated area
                               is returned in *addr.  Otherwise, an error code is returned
                               and *addr is undefined.
                   EINVAL   length is zero.
                   EINVAL   length is too large.
                   EFAULT   addr points to an invalid address.
                   ENOMEM   No memory is available or the process' maximum number of allocations
                            would have been exceeded.
        """
        # TODO: check 4 bytes from addr
        if addr not in cpu.memory:
            logger.info("ALLOCATE: addr points to invalid address. Returning EFAULT")
            return Decree.CGC_EFAULT

        perms = ['rw ', 'rwx'][bool(isX)]
        try:
            result = cpu.memory.mmap(None, length, perms)
        except Exception as e:
            logger.info("ALLOCATE exception %s. Returning ENOMEM %r", str(e), length)
            return Decree.CGC_ENOMEM
        cpu.write_int(addr, result, 32)
        logger.info("ALLOCATE(%d, %s, 0x%08x) -> 0x%08x" % (length, perms, addr, result))
        self.syscall_trace.append(("_allocate", -1, length))
        return 0