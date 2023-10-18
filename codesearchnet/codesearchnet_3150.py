def mmapFile(self, addr, size, perms, filename, offset=0):
        """
        Creates a new file mapping in the memory address space.

        :param addr: the starting address (took as hint). If C{addr} is C{0} the first big enough
                     chunk of memory will be selected as starting address.
        :param size: the contents of a file mapping are initialized using C{size} bytes starting
                     at offset C{offset} in the file C{filename}.
        :param perms: the access permissions to this memory.
        :param filename: the pathname to the file to map.
        :param offset: the contents of a file mapping are initialized using C{size} bytes starting
                      at offset C{offset} in the file C{filename}.
        :return: the starting address where the file was mapped.
        :rtype: int
        :raises error:
                   - 'Address shall be concrete' if C{addr} is not an integer number.
                   - 'Address too big' if C{addr} goes beyond the limit of the memory.
                   - 'Map already used' if the piece of memory starting in C{addr} and with length C{size} isn't free.
        """
        # If addr is NULL, the system determines where to allocate the region.
        assert addr is None or isinstance(addr, int), 'Address shall be concrete'
        assert addr < self.memory_size, 'Address too big'
        assert size > 0

        self.cpu._publish('will_map_memory', addr, size, perms, filename, offset)

        map = AnonMap(addr, size, perms)
        self._add(map)

        # address is rounded down to the nearest multiple of the allocation granularity
        if addr is not None:
            addr = self._floor(addr)

        # size value is rounded up to the next page boundary
        size = self._ceil(size)

        with open(filename, 'rb') as f:
            fdata = f.read()  # fdata is a bytes now

        # this worked
        fdata = fdata[offset:]
        fdata = fdata.ljust(size, b'\0')

        for i in range(size):
            Memory.write(self, addr + i, chr(fdata[i]), force=True)

        logger.debug('New file-memory map @%x size:%x', addr, size)
        self.cpu._publish('did_map_memory', addr, size, perms, filename, offset, addr)

        return addr