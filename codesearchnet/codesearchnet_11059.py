def transform(self, program: moderngl.Program, buffer: moderngl.Buffer,
                  mode=None, vertices=-1, first=0, instances=1):
        """
        Transform vertices. Stores the output in a single buffer.

        Args:
            program: The ``moderngl.Program``
            buffer: The ``moderngl.buffer`` to store the output

        Keyword Args:
            mode: Draw mode (for example ``moderngl.POINTS``)
            vertices (int): The number of vertices to transform
            first (int): The index of the first vertex to start with
            instances (int): The number of instances
        """
        vao = self.instance(program)

        if mode is None:
            mode = self.mode

        vao.transform(buffer, mode=mode, vertices=vertices, first=first, instances=instances)