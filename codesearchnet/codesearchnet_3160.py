def write_int(self, where, expression, size=None, force=False):
        """
        Writes int to memory

        :param int where: address to write to
        :param expr: value to write
        :type expr: int or BitVec
        :param size: bit size of `expr`
        :param force: whether to ignore memory permissions
        """
        if size is None:
            size = self.address_bit_size
        assert size in SANE_SIZES
        self._publish('will_write_memory', where, expression, size)

        data = [Operators.CHR(Operators.EXTRACT(expression, offset, 8)) for offset in range(0, size, 8)]
        self._memory.write(where, data, force)

        self._publish('did_write_memory', where, expression, size)