def instruction_to_svg_dict(self, instruction):
        """
        :return: an xml-dictionary with the same content as
          :meth:`instruction_to_svg`.
        """
        instruction_type = instruction.type
        if instruction_type in self._instruction_type_to_file_content:
            svg = self._instruction_type_to_file_content[instruction_type]
            return self._set_fills_in_color_layer(svg, instruction.hex_color)
        return self.default_instruction_to_svg_dict(instruction)