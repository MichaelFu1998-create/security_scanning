def sys_brk(self, brk):
        """
        Changes data segment size (moves the C{brk} to the new address)
        :rtype: int
        :param brk: the new address for C{brk}.
        :return: the value of the new C{brk}.
        :raises error:
                    - "Error in brk!" if there is any error allocating the memory
        """
        if brk != 0 and brk > self.elf_brk:
            mem = self.current.memory
            size = brk - self.brk
            if brk > mem._ceil(self.brk):
                perms = mem.perms(self.brk - 1)
                addr = mem.mmap(mem._ceil(self.brk), size, perms)
                if not mem._ceil(self.brk) == addr:
                    logger.error(f"Error in brk: ceil: {hex(mem._ceil(self.brk))} brk: {hex(brk)} self.brk: {hex(self.brk)} addr: {hex(addr)}")
                    return self.brk
            self.brk += size
        return self.brk