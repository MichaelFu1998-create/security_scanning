def _dump_knitting_pattern(self, file):
        """dump a knitting pattern to a file."""
        knitting_pattern_set = self.__on_dump()
        knitting_pattern = knitting_pattern_set.patterns.at(0)
        layout = GridLayout(knitting_pattern)
        builder = AYABPNGBuilder(*layout.bounding_box)
        builder.set_colors_in_grid(layout.walk_instructions())
        builder.write_to_file(file)