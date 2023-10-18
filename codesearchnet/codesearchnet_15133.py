def instruction_in_row(self, row, specification):
        """Parse an instruction.

        :param row: the row of the instruction
        :param specification: the specification of the instruction
        :return: the instruction in the row
        """
        whole_instruction_ = self._as_instruction(specification)
        return self._spec.new_instruction_in_row(row, whole_instruction_)