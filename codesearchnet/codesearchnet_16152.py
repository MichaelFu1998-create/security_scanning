def pack(self, *args):
        """See :func:`~bitstruct.pack()`.

        """

        # Sanity check of the number of arguments.
        if len(args) < self._number_of_arguments:
            raise Error(
                "pack expected {} item(s) for packing (got {})".format(
                    self._number_of_arguments,
                    len(args)))

        return self.pack_any(args)