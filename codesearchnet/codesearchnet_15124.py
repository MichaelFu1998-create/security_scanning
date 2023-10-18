def index_of_first_produced_mesh_in_row(self):
        """Index of the first produced mesh in the row that consumes it.

        :return: an index of the first produced mesh of rows produced meshes
        :rtype: int

        .. note:: If the instruction :meth:`produces meshes
          <Instruction.produces_meshes>`, this is the index of the first
          mesh the instruction produces in all the meshes of the row.
          If the instruction does not produce meshes, the index of the mesh is
          returned as if the instruction had produced a mesh.

        .. code::

            if instruction.produces_meshes():
                index = instruction.index_of_first_produced_mesh_in_row

        """
        index = 0
        for instruction in self.row_instructions:
            if instruction is self:
                break
            index += instruction.number_of_produced_meshes
        else:
            self._raise_not_found_error()
        return index