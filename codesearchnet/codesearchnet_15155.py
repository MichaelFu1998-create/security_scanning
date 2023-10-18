def _step(self, row, position, passed):
        """Walk through the knitting pattern by expanding an row."""
        if row in passed or not self._row_should_be_placed(row, position):
            return
        self._place_row(row, position)
        passed = [row] + passed
        # print("{}{} at\t{} {}".format("  " * len(passed), row, position,
        #                               passed))
        for i, produced_mesh in enumerate(row.produced_meshes):
            self._expand_produced_mesh(produced_mesh, i, position, passed)
        for i, consumed_mesh in enumerate(row.consumed_meshes):
            self._expand_consumed_mesh(consumed_mesh, i, position, passed)