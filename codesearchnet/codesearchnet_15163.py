def walk_instructions(self, mapping=identity):
        """Iterate over instructions.

        :return: an iterator over :class:`instructions in grid
          <InstructionInGrid>`
        :param mapping: funcion to map the result

        .. code:: python

            for pos, c in layout.walk_instructions(lambda i: (i.xy, i.color)):
                print("color {} at {}".format(c, pos))

        """
        instructions = chain(*self.walk_rows(lambda row: row.instructions))
        return map(mapping, instructions)