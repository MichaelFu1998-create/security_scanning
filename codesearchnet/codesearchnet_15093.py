def get_instruction_id(self, instruction_or_id):
        """The id that identifies the instruction in this cache.

        :param instruction_or_id: an :class:`instruction
          <knittingpattern.Instruction.Instruction>` or an instruction id
        :return: a :func:`hashable <hash>` object
        :rtype: tuple
        """
        if isinstance(instruction_or_id, tuple):
            return _InstructionId(instruction_or_id)
        return _InstructionId(instruction_or_id.type,
                              instruction_or_id.hex_color)