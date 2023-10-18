def draw(self):
        """Draw the shape in the current OpenGL context.

        """
        if self.enabled:
            self._vertex_list.colors = self._gl_colors
            self._vertex_list.vertices = self._gl_vertices
            self._vertex_list.draw(pyglet.gl.GL_TRIANGLES)