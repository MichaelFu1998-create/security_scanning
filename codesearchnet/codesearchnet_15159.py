def _place_row(self, row, position):
        """place the instruction on a grid"""
        self._rows_in_grid[row] = RowInGrid(row, position)