def add_instruction(self, specification):
        """Add an instruction specification

        :param specification: a specification with a key
          :data:`knittingpattern.Instruction.TYPE`

        .. seealso:: :meth:`as_instruction`
        """
        instruction = self.as_instruction(specification)
        self._type_to_instruction[instruction.type] = instruction