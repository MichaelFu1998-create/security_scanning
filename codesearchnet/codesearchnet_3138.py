def _search(self, size, start=None, counter=0):
        """
        Recursively searches the address space for enough free space to allocate C{size} bytes.

        :param size: the size in bytes to allocate.
        :param start: an address from where to start the search.
        :param counter: internal parameter to know if all the memory was already scanned.
        :return: the address of an available space to map C{size} bytes.
        :raises MemoryException: if there is no space available to allocate the desired memory.
        :rtype: int


        todo: Document what happens when you try to allocate something that goes round the address 32/64 bit representation.
        """
        assert size & self.page_mask == 0
        if start is None:
            end = {32: 0xf8000000, 64: 0x0000800000000000}[self.memory_bit_size]
            start = end - size
        else:
            if start > self.memory_size - size:
                start = self.memory_size - size
            end = start + size

        consecutive_free = 0
        for p in range(self._page(end - 1), -1, -1):
            if p not in self._page2map:
                consecutive_free += 0x1000
            else:
                consecutive_free = 0
            if consecutive_free >= size:
                return p << self.page_bit_size
            counter += 1
            if counter >= self.memory_size // self.page_size:
                raise MemoryException('Not enough memory')

        return self._search(size, self.memory_size - size, counter)