def add_point_light(self, position, radius):
        """Add point light"""
        self.point_lights.append(PointLight(position, radius))