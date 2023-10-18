def sys_munmap(self, addr, size):
        """
        Unmaps a file from memory. It deletes the mappings for the specified address range
        :rtype: int

        :param addr: the starting address to unmap.
        :param size: the size of the portion to unmap.
        :return: C{0} on success.
        """
        self.current.memory.munmap(addr, size)
        return 0