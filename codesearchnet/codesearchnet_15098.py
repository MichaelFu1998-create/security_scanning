def last_consumed_mesh(self):
        """The last consumed mesh.

        :return: the last consumed mesh
        :rtype: knittingpattern.Mesh.Mesh
        :raises IndexError: if no mesh is consumed

        .. seealso:: :attr:`number_of_consumed_meshes`
        """
        for instruction in reversed(self.instructions):
            if instruction.consumes_meshes():
                return instruction.last_consumed_mesh
        raise IndexError("{} consumes no meshes".format(self))