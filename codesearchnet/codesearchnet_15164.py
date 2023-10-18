def walk_rows(self, mapping=identity):
        """Iterate over rows.

        :return: an iterator over :class:`rows <RowsInGrid>`
        :param mapping: funcion to map the result, see
          :meth:`walk_instructions` for an example usage
        """
        row_in_grid = self._walk.row_in_grid
        return map(lambda row: mapping(row_in_grid(row)), self._rows)