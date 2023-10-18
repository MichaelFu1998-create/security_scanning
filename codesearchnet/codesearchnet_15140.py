def add_row(self, id_):
        """Add a new row to the pattern.

        :param id_: the id of the row
        """
        row = self._parser.new_row(id_)
        self._rows.append(row)
        return row