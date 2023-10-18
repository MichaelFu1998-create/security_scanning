def transfer_to_row(self, new_row):
        """Transfer this instruction to a new row.

        :param knittingpattern.Row.Row new_row: the new row the instruction is
          in.
        """
        if new_row != self._row:
            index = self.get_index_in_row()
            if index is not None:
                self._row.instructions.pop(index)
            self._row = new_row