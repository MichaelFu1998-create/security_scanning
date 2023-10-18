def instruction_in_grid(self, instruction):
        """Returns an `InstructionInGrid` object for the `instruction`"""
        row_position = self._rows_in_grid[instruction.row].xy
        x = instruction.index_of_first_consumed_mesh_in_row
        position = Point(row_position.x + x, row_position.y)
        return InstructionInGrid(instruction, position)