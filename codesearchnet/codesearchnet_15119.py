def add_new_pattern(self, id_, name=None):
        """Add a new, empty knitting pattern to the set.

        :param id_: the id of the pattern
        :param name: the name of the pattern to add or if :obj:`None`, the
          :paramref:`id_` is used
        :return: a new, empty knitting pattern
        :rtype: knittingpattern.KnittingPattern.KnittingPattern
        """
        if name is None:
            name = id_
        pattern = self._parser.new_pattern(id_, name)
        self._patterns.append(pattern)
        return pattern