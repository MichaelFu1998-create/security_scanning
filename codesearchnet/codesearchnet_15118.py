def to_svg(self, zoom):
        """Create an SVG from the knitting pattern set.

        :param float zoom: the height and width of a knit instruction
        :return: a dumper to save the svg to
        :rtype: knittingpattern.Dumper.XMLDumper

        Example:

        .. code:: python

            >>> knitting_pattern_set.to_svg(25).temporary_path(".svg")
            "/the/path/to/the/file.svg"
        """
        def on_dump():
            """Dump the knitting pattern to the file.

            :return: the SVG XML structure as dictionary.
            """
            knitting_pattern = self.patterns.at(0)
            layout = GridLayout(knitting_pattern)
            instruction_to_svg = default_instruction_svg_cache()
            builder = SVGBuilder()
            kp_to_svg = KnittingPatternToSVG(knitting_pattern, layout,
                                             instruction_to_svg, builder, zoom)
            return kp_to_svg.build_SVG_dict()
        return XMLDumper(on_dump)