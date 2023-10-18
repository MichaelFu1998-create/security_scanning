def draw(self, mesh, projection_matrix=None, view_matrix=None, camera_matrix=None, time=0):
        """
        Draw code for the mesh. Should be overriden.

        :param projection_matrix: projection_matrix (bytes)
        :param view_matrix: view_matrix (bytes)
        :param camera_matrix: camera_matrix (bytes)
        :param time: The current time
        """
        self.program["m_proj"].write(projection_matrix)
        self.program["m_mv"].write(view_matrix)
        mesh.vao.render(self.program)