def knitting_pattern(self, specification=None):
        """loads a :class:`knitting pattern
        <knittingpattern.KnittingPattern.KnittingPattern>` from the dumped
        content

        :param specification: a
          :class:`~knittingpattern.ParsingSpecification.ParsingSpecification`
          or :obj:`None` to use the default specification"""
        from ..ParsingSpecification import new_knitting_pattern_set_loader
        if specification is None:
            loader = new_knitting_pattern_set_loader()
        else:
            loader = new_knitting_pattern_set_loader(specification)
        return loader.object(self.object())