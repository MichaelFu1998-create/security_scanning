def draw(self, projection_matrix=None, view_matrix=None, camera_matrix=None, time=0):
        """
        Draw the mesh using the assigned mesh program

        :param projection_matrix: projection_matrix (bytes)
        :param view_matrix: view_matrix (bytes)
        :param camera_matrix: camera_matrix (bytes)
        """
        if self.mesh_program:
            self.mesh_program.draw(
                self,
                projection_matrix=projection_matrix,
                view_matrix=view_matrix,
                camera_matrix=camera_matrix,
                time=time
            )