def _ceil(self, address):
        """
        Returns the smallest page boundary value not less than the address.
        :rtype: int
        :param address: the address to calculate its ceil.
        :return: the ceil of C{address}.
        """
        return (((address - 1) + self.page_size) & ~self.page_mask) & self.memory_mask