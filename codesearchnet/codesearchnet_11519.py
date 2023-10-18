def _base_repr(self, and_also=None):
        """Common repr logic for subclasses to hook
        """
        items = [
            "=".join((key, repr(getattr(self, key))))
            for key in sorted(self._fields.keys())]

        if items:
            output = ", ".join(items)
        else:
            output = None

        if and_also:
            return "{}({}, {})".format(self.__class__.__name__,
                                       output, and_also)
        else:
            return "{}({})".format(self.__class__.__name__, output)