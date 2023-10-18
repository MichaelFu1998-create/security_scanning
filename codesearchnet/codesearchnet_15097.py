def last_produced_mesh(self):
        """The last produced mesh.

        :return: the last produced mesh
        :rtype: knittingpattern.Mesh.Mesh
        :raises IndexError: if no mesh is produced

        .. seealso:: :attr:`number_of_produced_meshes`
        """
        for instruction in reversed(self.instructions):
            if instruction.produces_meshes():
                return instruction.last_produced_mesh
        raise IndexError("{} produces no meshes".format(self))