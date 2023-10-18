def _register_instruction_in_defs(self, instruction):
        """Create a definition for the instruction.

        :return: the id of a symbol in the defs for the specified
          :paramref:`instruction`
        :rtype: str

        If no symbol yet exists in the defs for the :paramref:`instruction` a
        symbol is created and saved using :meth:`_make_symbol`.
        """
        type_ = instruction.type
        color_ = instruction.color
        instruction_to_svg_dict = \
            self._instruction_to_svg.instruction_to_svg_dict
        instruction_id = "{}:{}".format(type_, color_)
        defs_id = instruction_id + ":defs"
        if instruction_id not in self._instruction_type_color_to_symbol:
            svg_dict = instruction_to_svg_dict(instruction)
            self._compute_scale(instruction_id, svg_dict)
            symbol = self._make_definition(svg_dict, instruction_id)
            self._instruction_type_color_to_symbol[defs_id] = \
                symbol[DEFINITION_HOLDER].pop("defs", {})
            self._instruction_type_color_to_symbol[instruction_id] = symbol
        return instruction_id