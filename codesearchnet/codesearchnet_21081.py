def _set_range(self, start, stop, value, value_len):
        """
        Assumes that start and stop are already in 'buffer' coordinates. value is a byte iterable.
        value_len is fractional.
        """
        assert stop >= start and value_len >= 0
        range_len = stop - start
        if range_len < value_len:
            self._insert_zeros(stop, stop + value_len - range_len)
            self._copy_to_range(start, value, value_len)
        elif range_len > value_len:
            self._del_range(stop - (range_len - value_len), stop)
            self._copy_to_range(start, value, value_len)
        else:
            self._copy_to_range(start, value, value_len)