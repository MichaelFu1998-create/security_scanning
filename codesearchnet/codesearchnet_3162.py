def read_int(self, where, size=None, force=False):
        """
        Reads int from memory

        :param int where: address to read from
        :param size: number of bits to read
        :return: the value read
        :rtype: int or BitVec
        :param force: whether to ignore memory permissions
        """
        if size is None:
            size = self.address_bit_size
        assert size in SANE_SIZES
        self._publish('will_read_memory', where, size)

        data = self._memory.read(where, size // 8, force)
        assert (8 * len(data)) == size
        value = Operators.CONCAT(size, *map(Operators.ORD, reversed(data)))

        self._publish('did_read_memory', where, value, size)
        return value