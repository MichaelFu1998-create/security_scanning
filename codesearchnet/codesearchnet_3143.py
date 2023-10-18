def _maps_in_range(self, start, end):
        """
        Generates the list of maps that overlaps with the range [start:end]
        """

        # Search for the first matching map
        addr = start
        while addr < end:
            if addr not in self:
                addr += self.page_size
            else:
                m = self._page2map[self._page(addr)]
                yield m
                addr = m.end