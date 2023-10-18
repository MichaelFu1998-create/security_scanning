def pack_into(self, buf, offset, data, **kwargs):
        """See :func:`~bitstruct.pack_into_dict()`.

        """

        try:
            self.pack_into_any(buf, offset, data, **kwargs)
        except KeyError as e:
            raise Error('{} not found in data dictionary'.format(str(e)))