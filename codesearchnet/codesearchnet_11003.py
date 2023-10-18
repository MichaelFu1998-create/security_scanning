def update(self, aspect_ratio=None, fov=None, near=None, far=None):
        """
        Update the internal projection matrix based on current values
        or values passed in if specified.

        :param aspect_ratio: New aspect ratio
        :param fov: New field of view
        :param near: New near value
        :param far: New far value
        """
        self.aspect_ratio = aspect_ratio or self.aspect_ratio
        self.fov = fov or self.fov
        self.near = near or self.near
        self.far = far or self.far

        self.matrix = Matrix44.perspective_projection(self.fov, self.aspect_ratio, self.near, self.far)