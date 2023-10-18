def as_instruction(self, specification):
        """Convert the specification into an instruction

        :param specification: a specification with a key
          :data:`knittingpattern.Instruction.TYPE`

        The instruction is not added.

        .. seealso:: :meth:`add_instruction`
        """
        instruction = self._instruction_class(specification)
        type_ = instruction.type
        if type_ in self._type_to_instruction:
            instruction.inherit_from(self._type_to_instruction[type_])
        return instruction