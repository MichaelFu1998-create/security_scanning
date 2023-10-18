def next_instruction_in_row(self):
        """The instruction after this one or None.

        :return: the instruction in :attr:`row_instructions` after this or
          :obj:`None` if this is the last
        :rtype: knittingpattern.Instruction.InstructionInRow

        This can be used to traverse the instructions.

        .. seealso:: :attr:`previous_instruction_in_row`
        """
        index = self.index_in_row + 1
        if index >= len(self.row_instructions):
            return None
        return self.row_instructions[index]