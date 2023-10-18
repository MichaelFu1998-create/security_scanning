def render(self, program: moderngl.Program, mode=None, vertices=-1, first=0, instances=1):
        """
        Render the VAO.

        Args:
            program: The ``moderngl.Program``

        Keyword Args:
            mode: Override the draw mode (``TRIANGLES`` etc)
            vertices (int): The number of vertices to transform
            first (int): The index of the first vertex to start with
            instances (int): The number of instances
        """
        vao = self.instance(program)

        if mode is None:
            mode = self.mode

        vao.render(mode, vertices=vertices, first=first, instances=instances)