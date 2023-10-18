def rows_before(self):
        """The rows that produce meshes for this row.

        :rtype: list
        :return: a list of rows that produce meshes for this row. Each row
          occurs only once. They are sorted by the first occurrence in the
          instructions.
        """
        rows_before = []
        for mesh in self.consumed_meshes:
            if mesh.is_produced():
                row = mesh.producing_row
                if rows_before not in rows_before:
                    rows_before.append(row)
        return rows_before