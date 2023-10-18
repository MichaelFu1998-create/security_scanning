def render_indirect(self, program: moderngl.Program, buffer, mode=None, count=-1, *, first=0):
        """
        The render primitive (mode) must be the same as the input primitive of the GeometryShader.
        The draw commands are 5 integers: (count, instanceCount, firstIndex, baseVertex, baseInstance).

        Args:
            program: The ``moderngl.Program``
            buffer: The ``moderngl.Buffer`` containing indirect draw commands

        Keyword Args:
            mode (int): By default :py:data:`TRIANGLES` will be used.
            count (int): The number of draws.
            first (int): The index of the first indirect draw command.
        """
        vao = self.instance(program)

        if mode is None:
            mode = self.mode

        vao.render_indirect(buffer, mode=mode, count=count, first=first)