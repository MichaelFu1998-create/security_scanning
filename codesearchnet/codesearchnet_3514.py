def sys_deallocate(self, cpu, addr, size):
        """ deallocate - remove allocations
        The  deallocate  system call deletes the allocations for the specified
        address range, and causes further references to the addresses within the
        range to generate invalid memory accesses. The region is also
        automatically deallocated when the process is terminated.

        The address addr must be a multiple of the page size.  The length parameter
        specifies the size of the region to be deallocated in bytes.  All pages
        containing a part of the indicated range are deallocated, and subsequent
        references will terminate the process.  It is not an error if the indicated
        range does not contain any allocated pages.

        The deallocate function is invoked through system call number 6.

        :param cpu: current CPU
        :param addr: the starting address to unmap.
        :param size: the size of the portion to unmap.
        :return 0        On success
                EINVAL   addr is not page aligned.
                EINVAL   length is zero.
                EINVAL   any  part  of  the  region  being  deallocated  is outside the valid
                         address range of the process.

        :param cpu: current CPU.
        :return: C{0} on success.
        """
        logger.info("DEALLOCATE(0x%08x, %d)" % (addr, size))

        if addr & 0xfff != 0:
            logger.info("DEALLOCATE: addr is not page aligned")
            return Decree.CGC_EINVAL
        if size == 0:
            logger.info("DEALLOCATE:length is zero")
            return Decree.CGC_EINVAL
        # unlikely AND WRONG!!!
        # if addr > Decree.CGC_SSIZE_MAX or addr+size > Decree.CGC_SSIZE_MAX:
        #    logger.info("DEALLOCATE: part of the region being deallocated is outside the valid address range of the process")
        #    return Decree.CGC_EINVAL

        cpu.memory.munmap(addr, size)
        self.syscall_trace.append(("_deallocate", -1, size))
        return 0