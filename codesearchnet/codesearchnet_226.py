def on(self, image):
        """
        Project polygons from one image to a new one.

        Parameters
        ----------
        image : ndarray or tuple of int
            New image onto which the polygons are to be projected.
            May also simply be that new image's shape tuple.

        Returns
        -------
        imgaug.PolygonsOnImage
            Object containing all projected polygons.

        """
        shape = normalize_shape(image)
        if shape[0:2] == self.shape[0:2]:
            return self.deepcopy()
        polygons = [poly.project(self.shape, shape) for poly in self.polygons]
        # TODO use deepcopy() here
        return PolygonsOnImage(polygons, shape)