def rows_after(self):
        """The rows that consume meshes from this row.

        :rtype: list
        :return: a list of rows that consume meshes from this row. Each row
          occurs only once. They are sorted by the first occurrence in the
          instructions.
        """
        rows_after = []
        for mesh in self.produced_meshes:
            if mesh.is_consumed():
                row = mesh.consuming_row
                if rows_after not in rows_after:
                    rows_after.append(row)
        return rows_after