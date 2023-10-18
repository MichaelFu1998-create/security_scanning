def munmap(self, start, size):
        """
        Deletes the mappings for the specified address range and causes further
        references to addresses within the range to generate invalid memory
        references.

        :param start: the starting address to delete.
        :param size: the length of the unmapping.
        """
        for addr in range(start, start + size):
            if len(self._symbols) == 0:
                break
            if addr in self._symbols:
                del self._symbols[addr]
        super().munmap(start, size)