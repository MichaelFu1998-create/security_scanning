def index_of_first_consumed_mesh_in_row(self):
        """The index of the first consumed mesh of this instruction in its row.

        Same as :attr:`index_of_first_produced_mesh_in_row`
        but for consumed meshes.
        """
        index = 0
        for instruction in self.row_instructions:
            if instruction is self:
                break
            index += instruction.number_of_consumed_meshes
        else:
            self._raise_not_found_error()
        return index