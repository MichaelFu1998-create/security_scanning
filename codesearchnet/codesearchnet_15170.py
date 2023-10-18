def default_instruction_to_svg(self, instruction):
        """As :meth:`instruction_to_svg` but it only takes the ``default.svg``
        file into account.

        In case no file is found for an instruction in
        :meth:`instruction_to_svg`,
        this method is used to determine the default svg for it.

        The content is created by replacing the text ``{instruction.type}`` in
        the whole svg file named ``default.svg``.

        If no file ``default.svg`` was loaded, an empty string is returned.
        """
        svg_dict = self.default_instruction_to_svg_dict(instruction)
        return xmltodict.unparse(svg_dict)