def _make_definition(self, svg_dict, instruction_id):
        """Create a symbol out of the supplied :paramref:`svg_dict`.

        :param dict svg_dict: dictionary containing the SVG for the
          instruction currently processed
        :param str instruction_id: id that will be assigned to the symbol
        """
        instruction_def = svg_dict["svg"]
        blacklisted_elements = ["sodipodi:namedview", "metadata"]
        whitelisted_attributes = ["@sodipodi:docname"]
        symbol = OrderedDict({"@id": instruction_id})
        for content, value in instruction_def.items():
            if content.startswith('@'):
                if content in whitelisted_attributes:
                    symbol[content] = value
            elif content not in blacklisted_elements:
                symbol[content] = value
        return {DEFINITION_HOLDER: symbol}