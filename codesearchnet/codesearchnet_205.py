def project(self, from_shape, to_shape):
        """
        Project the polygon onto an image with different shape.

        The relative coordinates of all points remain the same.
        E.g. a point at (x=20, y=20) on an image (width=100, height=200) will be
        projected on a new image (width=200, height=100) to (x=40, y=10).

        This is intended for cases where the original image is resized.
        It cannot be used for more complex changes (e.g. padding, cropping).

        Parameters
        ----------
        from_shape : tuple of int
            Shape of the original image. (Before resize.)

        to_shape : tuple of int
            Shape of the new image. (After resize.)

        Returns
        -------
        imgaug.Polygon
            Polygon object with new coordinates.

        """
        if from_shape[0:2] == to_shape[0:2]:
            return self.copy()
        ls_proj = self.to_line_string(closed=False).project(
            from_shape, to_shape)
        return self.copy(exterior=ls_proj.coords)