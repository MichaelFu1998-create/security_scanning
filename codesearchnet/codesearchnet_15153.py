def instructions(self):
        """The instructions in a grid.

        :return: the :class:`instructions in a grid <InstructionInGrid>` of
          this row
        :rtype: list
        """
        x = self.x
        y = self.y
        result = []
        for instruction in self._row.instructions:
            instruction_in_grid = InstructionInGrid(instruction, Point(x, y))
            x += instruction_in_grid.width
            result.append(instruction_in_grid)
        return result