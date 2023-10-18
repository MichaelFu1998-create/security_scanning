def map_containing(self, address):
        """
        Returns the L{MMap} object containing the address.

        :param address: the address to obtain its mapping.
        :rtype: L{MMap}

        @todo: symbolic address
        """
        page_offset = self._page(address)
        if page_offset not in self._page2map:
            raise MemoryException("Page not mapped", address)
        return self._page2map[page_offset]