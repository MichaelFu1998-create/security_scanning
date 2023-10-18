def calc_global_bbox(self, view_matrix, bbox_min, bbox_max):
        """Recursive calculation of scene bbox"""
        if self.matrix is not None:
            view_matrix = matrix44.multiply(self.matrix, view_matrix)

        if self.mesh:
            bbox_min, bbox_max = self.mesh.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        for child in self.children:
            bbox_min, bbox_max = child.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        return bbox_min, bbox_max