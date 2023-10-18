def instance(self, program: moderngl.Program) -> moderngl.VertexArray:
        """
        Obtain the ``moderngl.VertexArray`` instance for the program.
        The instance is only created once and cached internally.

        Returns: ``moderngl.VertexArray`` instance
        """
        vao = self.vaos.get(program.glo)
        if vao:
            return vao

        program_attributes = [name for name, attr in program._members.items() if isinstance(attr, moderngl.Attribute)]

        # Make sure all attributes are covered
        for attrib_name in program_attributes:
            # Ignore built in attributes for now
            if attrib_name.startswith('gl_'):
                continue

            # Do we have a buffer mapping to this attribute?
            if not sum(buffer.has_attribute(attrib_name) for buffer in self.buffers):
                raise VAOError("VAO {} doesn't have attribute {} for program {}".format(
                    self.name, attrib_name, program.name))

        vao_content = []

        # Pick out the attributes we can actually map
        for buffer in self.buffers:
            content = buffer.content(program_attributes)
            if content:
                vao_content.append(content)

        # Any attribute left is not accounted for
        if program_attributes:
            for attrib_name in program_attributes:
                if attrib_name.startswith('gl_'):
                    continue

                raise VAOError("Did not find a buffer mapping for {}".format([n for n in program_attributes]))

        # Create the vao
        if self._index_buffer:
            vao = context.ctx().vertex_array(program, vao_content,
                                             self._index_buffer, self._index_element_size)
        else:
            vao = context.ctx().vertex_array(program, vao_content)

        self.vaos[program.glo] = vao
        return vao