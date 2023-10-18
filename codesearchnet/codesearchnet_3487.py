def sys_mmap(self, address, size, prot, flags, fd, offset):
        """
        Creates a new mapping in the virtual address space of the calling process.
        :rtype: int

        :param address: the starting address for the new mapping. This address is used as hint unless the
                        flag contains C{MAP_FIXED}.
        :param size: the length of the mapping.
        :param prot: the desired memory protection of the mapping.
        :param flags: determines whether updates to the mapping are visible to other
                      processes mapping the same region, and whether updates are carried
                      through to the underlying file.
        :param fd: the contents of a file mapping are initialized using C{size} bytes starting at
                   offset C{offset} in the file referred to by the file descriptor C{fd}.
        :param offset: the contents of a file mapping are initialized using C{size} bytes starting at
                       offset C{offset} in the file referred to by the file descriptor C{fd}.
        :return:
                - C{-1} in case you use C{MAP_FIXED} in the flags and the mapping can not be place at the desired address.
                - the address of the new mapping (that must be the same as address in case you included C{MAP_FIXED} in flags).
        :todo: handle exception.
        """

        if address == 0:
            address = None

        cpu = self.current
        if flags & 0x10:
            cpu.memory.munmap(address, size)

        perms = perms_from_protflags(prot)

        if flags & 0x20:
            result = cpu.memory.mmap(address, size, perms)
        elif fd == 0:
            assert offset == 0
            result = cpu.memory.mmap(address, size, perms)
            data = self.files[fd].read(size)
            cpu.write_bytes(result, data)
        else:
            # FIXME Check if file should be symbolic input and do as with fd0
            result = cpu.memory.mmapFile(address, size, perms, self.files[fd].name, offset)

        actually_mapped = f'0x{result:016x}'
        if address is None or result != address:
            address = address or 0
            actually_mapped += f' [requested: 0x{address:016x}]'

        if flags & 0x10 != 0 and result != address:
            cpu.memory.munmap(result, size)
            result = -1

        return result