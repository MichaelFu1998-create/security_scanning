def window_at(self, geom, window_shape):
        """Return a subsetted window of a given size, centered on a geometry object

        Useful for generating training sets from vector training data
        Will throw a ValueError if the window is not within the image bounds

        Args:
            geom (shapely,geometry): Geometry to center the image on
            window_shape (tuple): The desired shape of the image as (height, width) in pixels.

        Returns:
            image: image object of same type
        """
        # Centroids of the input geometry may not be centered on the object.
        # For a covering image we use the bounds instead.
        # This is also a workaround for issue 387.
        y_size, x_size = window_shape[0], window_shape[1]
        bounds = box(*geom.bounds)
        px = ops.transform(self.__geo_transform__.rev, bounds).centroid
        miny, maxy = int(px.y - y_size/2), int(px.y + y_size/2)
        minx, maxx = int(px.x - x_size/2), int(px.x + x_size/2)
        _, y_max, x_max = self.shape
        if minx < 0 or miny < 0 or maxx > x_max or maxy > y_max:
            raise ValueError("Input geometry resulted in a window outside of the image")
        return self[:, miny:maxy, minx:maxx]