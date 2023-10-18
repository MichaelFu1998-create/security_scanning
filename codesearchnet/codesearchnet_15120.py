def to_svg(self, converter=None):
        """Return a SVGDumper for this instruction.

        :param converter: a :class:`
          knittingpattern.convert.InstructionSVGCache.InstructionSVGCache` or
          :obj:`None`. If :obj:`None` is given, the :func:`
          knittingpattern.convert.InstructionSVGCache.default_svg_cache` is
          used.
        :rtype: knittingpattern.Dumper.SVGDumper
        """
        if converter is None:
            from knittingpattern.convert.InstructionSVGCache import \
                default_svg_cache
            converter = default_svg_cache()
        return converter.to_svg(self)