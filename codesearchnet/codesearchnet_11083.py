def create(self):
        """
        Creates a shader program.

        Returns:
            ModernGL Program instance
        """
        # Get out varyings
        out_attribs = []

        # If no fragment shader is present we are doing transform feedback
        if not self.fragment_source:
            # Out attributes is present in geometry shader if present
            if self.geometry_source:
                out_attribs = self.geometry_source.find_out_attribs()
            # Otherwise they are specified in vertex shader
            else:
                out_attribs = self.vertex_source.find_out_attribs()

        program = self.ctx.program(
            vertex_shader=self.vertex_source.source,
            geometry_shader=self.geometry_source.source if self.geometry_source else None,
            fragment_shader=self.fragment_source.source if self.fragment_source else None,
            tess_control_shader=self.tess_control_source.source if self.tess_control_source else None,
            tess_evaluation_shader=self.tess_evaluation_source.source if self.tess_evaluation_source else None,
            varyings=out_attribs,
        )
        program.extra = {'meta': self.meta}
        return program