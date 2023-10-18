def _row_should_be_placed(self, row, position):
        """:return: whether to place this instruction"""
        placed_row = self._rows_in_grid.get(row)
        return placed_row is None or placed_row.y < position.y