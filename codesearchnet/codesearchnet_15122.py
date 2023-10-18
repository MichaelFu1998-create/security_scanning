def get_index_in_row(self):
        """Index of the instruction in the instructions of the row or None.

        :return: index in the :attr:`row`'s instructions or None, if the
          instruction is not in the row
        :rtype: int

        .. seealso:: :attr:`row_instructions`, :attr:`index_in_row`,
          :meth:`is_in_row`
        """
        expected_index = self._cached_index_in_row
        instructions = self._row.instructions
        if expected_index is not None and \
                0 <= expected_index < len(instructions) and \
                instructions[expected_index] is self:
            return expected_index
        for index, instruction_in_row in enumerate(instructions):
            if instruction_in_row is self:
                self._cached_index_in_row = index
                return index
        return None