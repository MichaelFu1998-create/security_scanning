def sys_mprotect(self, start, size, prot):
        """
        Sets protection on a region of memory. Changes protection for the calling process's
        memory page(s) containing any part of the address range in the interval [C{start}, C{start}+C{size}-1].
        :rtype: int

        :param start: the starting address to change the permissions.
        :param size: the size of the portion of memory to change the permissions.
        :param prot: the new access permission for the memory.
        :return: C{0} on success.
        """
        perms = perms_from_protflags(prot)
        ret = self.current.memory.mprotect(start, size, perms)
        return 0