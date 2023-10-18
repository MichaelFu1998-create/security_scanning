def knitting_pattern_set(self, values):
        """Parse a knitting pattern set.

        :param dict value: the specification of the knitting pattern set
        :rtype: knittingpattern.KnittingPatternSet.KnittingPatternSet
        :raises knittingpattern.KnittingPatternSet.ParsingError: if
          :paramref:`value` does not fulfill the :ref:`specification
          <FileFormatSpecification>`.

        """
        self._start()
        pattern_collection = self._new_pattern_collection()
        self._fill_pattern_collection(pattern_collection, values)
        self._create_pattern_set(pattern_collection, values)
        return self._pattern_set