def mmap(self, addr, size, perms, data_init=None, name=None):
        """
        Creates a new mapping in the memory address space.

        :param addr: the starting address (took as hint). If C{addr} is C{0} the first big enough
                     chunk of memory will be selected as starting address.
        :param size: the length of the mapping.
        :param perms: the access permissions to this memory.
        :param data_init: optional data to initialize this memory.
        :param name: optional name to give to this mapping
        :return: the starting address where the memory was mapped.
        :raises error:
                   - 'Address shall be concrete' if C{addr} is not an integer number.
                   - 'Address too big' if C{addr} goes beyond the limit of the memory.
                   - 'Map already used' if the piece of memory starting in C{addr} and with length C{size} isn't free.
        :rtype: int

        """
        # If addr is NULL, the system determines where to allocate the region.
        assert addr is None or isinstance(addr, int), 'Address shall be concrete'

        self.cpu._publish('will_map_memory', addr, size, perms, None, None)

        # address is rounded down to the nearest multiple of the allocation granularity
        if addr is not None:
            assert addr < self.memory_size, 'Address too big'
            addr = self._floor(addr)

        # size value is rounded up to the next page boundary
        size = self._ceil(size)

        # If zero search for a spot
        addr = self._search(size, addr)

        # It should not be allocated
        for i in range(self._page(addr), self._page(addr + size)):
            assert i not in self._page2map, 'Map already used'

        # Create the anonymous map
        m = AnonMap(start=addr, size=size, perms=perms, data_init=data_init, name=name)

        # Okay, ready to alloc
        self._add(m)

        logger.debug('New memory map @%x size:%x', addr, size)

        self.cpu._publish('did_map_memory', addr, size, perms, None, None, addr)
        return addr