def unpack_from(self, data, offset=0):
        """See :func:`~bitstruct.unpack_from_dict()`.

        """

        return {info.name: v for info, v in self.unpack_from_any(data, offset)}