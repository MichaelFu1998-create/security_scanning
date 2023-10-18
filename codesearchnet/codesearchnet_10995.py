def create_projection(self, fov: float = 75.0, near: float = 1.0, far: float = 100.0, aspect_ratio: float = None):
        """
        Create a projection matrix with the following parameters.
        When ``aspect_ratio`` is not provided the configured aspect
        ratio for the window will be used.

        Args:
            fov (float): Field of view (float)
            near (float): Camera near value
            far (float): Camrea far value

        Keyword Args:
            aspect_ratio (float): Aspect ratio of the viewport

        Returns:
            The projection matrix as a float32 :py:class:`numpy.array`
        """
        return matrix44.create_perspective_projection_matrix(
            fov,
            aspect_ratio or self.window.aspect_ratio,
            near,
            far,
            dtype='f4',
        )