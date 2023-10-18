def instruction_to_svg_dict(self, instruction_or_id, copy_result=True):
        """Return the SVG dict for the SVGBuilder.

        :param instruction_or_id: the instruction or id, see
          :meth:`get_instruction_id`
        :param bool copy_result: whether to copy the result
        :rtype: dict

        The result is cached.
        """
        instruction_id = self.get_instruction_id(instruction_or_id)
        if instruction_id in self._cache:
            result = self._cache[instruction_id]
        else:
            result = self._instruction_to_svg_dict(instruction_id)
            self._cache[instruction_id] = result
        if copy_result:
            result = deepcopy(result)
        return result