def first_consumed_mesh(self):
        """The first consumed mesh.

        :return: the first consumed mesh
        :rtype: knittingpattern.Mesh.Mesh
        :raises IndexError: if no mesh is consumed

        .. seealso:: :attr:`number_of_consumed_meshes`
        """
        for instruction in self.instructions:
            if instruction.consumes_meshes():
                return instruction.first_consumed_mesh
        raise IndexError("{} consumes no meshes".format(self))