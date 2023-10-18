def pack_into(self, buf, offset, *args, **kwargs):
        """See :func:`~bitstruct.pack_into()`.

        """

        # Sanity check of the number of arguments.
        if len(args) < self._number_of_arguments:
            raise Error(
                "pack expected {} item(s) for packing (got {})".format(
                    self._number_of_arguments,
                    len(args)))

        self.pack_into_any(buf, offset, args, **kwargs)