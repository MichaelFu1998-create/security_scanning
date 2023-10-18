def default_instruction_to_svg_dict(self, instruction):
        """Returns an xml-dictionary with the same content as
        :meth:`default_instruction_to_svg`

        If no file ``default.svg`` was loaded, an empty svg-dict is returned.
        """
        instruction_type = instruction.type
        default_type = "default"
        rep_str = "{instruction.type}"
        if default_type not in self._instruction_type_to_file_content:
            return {"svg": ""}
        default_svg = self._instruction_type_to_file_content[default_type]
        default_svg = default_svg.replace(rep_str, instruction_type)
        colored_svg = self._set_fills_in_color_layer(default_svg,
                                                     instruction.hex_color)
        return colored_svg