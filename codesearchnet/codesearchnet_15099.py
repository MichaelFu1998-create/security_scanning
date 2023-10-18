def first_produced_mesh(self):
        """The first produced mesh.

        :return: the first produced mesh
        :rtype: knittingpattern.Mesh.Mesh
        :raises IndexError: if no mesh is produced

        .. seealso:: :attr:`number_of_produced_meshes`
        """
        for instruction in self.instructions:
            if instruction.produces_meshes():
                return instruction.first_produced_mesh
        raise IndexError("{} produces no meshes".format(self))