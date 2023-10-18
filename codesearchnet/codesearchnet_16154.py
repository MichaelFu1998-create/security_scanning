def unpack_from(self, data, offset=0):
        """See :func:`~bitstruct.unpack_from()`.

        """

        return tuple([v[1] for v in self.unpack_from_any(data, offset)])