def draw_bbox(self, projection_matrix=None, camera_matrix=None, all=True):
        """Draw scene and mesh bounding boxes"""
        projection_matrix = projection_matrix.astype('f4').tobytes()
        camera_matrix = camera_matrix.astype('f4').tobytes()

        # Scene bounding box
        self.bbox_program["m_proj"].write(projection_matrix)
        self.bbox_program["m_view"].write(self._view_matrix.astype('f4').tobytes())
        self.bbox_program["m_cam"].write(camera_matrix)
        self.bbox_program["bb_min"].write(self.bbox_min.astype('f4').tobytes())
        self.bbox_program["bb_max"].write(self.bbox_max.astype('f4').tobytes())
        self.bbox_program["color"].value = (1.0, 0.0, 0.0)
        self.bbox_vao.render(self.bbox_program)

        if not all:
            return

        # Draw bounding box for children
        for node in self.root_nodes:
            node.draw_bbox(projection_matrix, camera_matrix, self.bbox_program, self.bbox_vao)