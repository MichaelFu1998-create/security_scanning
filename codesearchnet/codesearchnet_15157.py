def _expand_produced_mesh(self, mesh, mesh_index, row_position, passed):
        """expand the produced meshes"""
        if not mesh.is_consumed():
            return
        row = mesh.consuming_row
        position = Point(
            row_position.x - mesh.index_in_consuming_row + mesh_index,
            row_position.y + INSTRUCTION_HEIGHT
        )
        self._expand(row, position, passed)