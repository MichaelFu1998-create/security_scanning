def draw(self, projection_matrix=None, camera_matrix=None, time=0):
        """
        Draw all the nodes in the scene

        :param projection_matrix: projection matrix (bytes)
        :param camera_matrix: camera_matrix (bytes)
        :param time: The current time
        """
        projection_matrix = projection_matrix.astype('f4').tobytes()
        camera_matrix = camera_matrix.astype('f4').tobytes()

        for node in self.root_nodes:
            node.draw(
                projection_matrix=projection_matrix,
                camera_matrix=camera_matrix,
                time=time,
            )

        self.ctx.clear_samplers(0, 4)