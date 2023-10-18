def new_pattern(self, id_, name, rows=None):
        """Create a new knitting pattern.

        If rows is :obj:`None` it is replaced with the
        :meth:`new_row_collection`.
        """
        if rows is None:
            rows = self.new_row_collection()
        return self._spec.new_pattern(id_, name, rows, self)