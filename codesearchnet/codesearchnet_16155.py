def pack(self, data):
        """See :func:`~bitstruct.pack_dict()`.

        """

        try:
            return self.pack_any(data)
        except KeyError as e:
            raise Error('{} not found in data dictionary'.format(str(e)))