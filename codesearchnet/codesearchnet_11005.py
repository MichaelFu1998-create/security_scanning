def draw(self, projection_matrix=None, camera_matrix=None, time=0):
        """
        Draw node and children

        :param projection_matrix: projection matrix (bytes)
        :param camera_matrix: camera_matrix (bytes)
        :param time: The current time
        """
        if self.mesh:
            self.mesh.draw(
                projection_matrix=projection_matrix,
                view_matrix=self.matrix_global_bytes,
                camera_matrix=camera_matrix,
                time=time
            )

        for child in self.children:
            child.draw(
                projection_matrix=projection_matrix,
                camera_matrix=camera_matrix,
                time=time
            )