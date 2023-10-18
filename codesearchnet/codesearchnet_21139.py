def byte_offset(self, bytes):
        """
        Maps `bytes` length to a sequence's offset. For example, if we do byte_offset(5) and our list of sequences is
        [(0, 2), (10, 11), (40, 45)] then the returned value will be 42.
        Note that `bytes` must be <= byte_length().
        :returns: actual offset in one of the sequences in the range for request byte length.
        :rtype: int or float
        """
        remaining_bytes = bytes
        for r in self:
            if r.is_open() or r.byte_length() >= remaining_bytes:
                return r.start + remaining_bytes
            else:
                remaining_bytes -= r.byte_length()
        assert False, "requested byte offset {0!r} is outside the range list {1!r}".format(bytes, self)