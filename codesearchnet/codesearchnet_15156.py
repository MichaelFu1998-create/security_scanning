def _expand_consumed_mesh(self, mesh, mesh_index, row_position, passed):
        """expand the consumed meshes"""
        if not mesh.is_produced():
            return
        row = mesh.producing_row
        position = Point(
            row_position.x + mesh.index_in_producing_row - mesh_index,
            row_position.y - INSTRUCTION_HEIGHT
        )
        self._expand(row, position, passed)