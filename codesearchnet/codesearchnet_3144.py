def munmap(self, start, size):
        """
        Deletes the mappings for the specified address range and causes further
        references to addresses within the range to generate invalid memory
        references.

        :param start: the starting address to delete.
        :param size: the length of the unmapping.
        """
        start = self._floor(start)
        end = self._ceil(start + size)

        self.cpu._publish('will_unmap_memory', start, size)

        for m in self._maps_in_range(start, end):
            self._del(m)
            head, tail = m.split(start)
            middle, tail = tail.split(end)
            assert middle is not None
            if head:
                self._add(head)
            if tail:
                self._add(tail)

        self.cpu._publish('did_unmap_memory', start, size)
        logger.debug(f'Unmap memory @{start:x} size:{size:x}')