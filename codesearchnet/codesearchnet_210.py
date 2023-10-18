def clip_out_of_image(self, image):
        """
        Cut off all parts of the polygon that are outside of the image.

        This operation may lead to new points being created.
        As a single polygon may be split into multiple new polygons, the result
        is always a list, which may contain more than one output polygon.

        This operation will return an empty list if the polygon is completely
        outside of the image plane.

        Parameters
        ----------
        image : (H,W,...) ndarray or tuple of int
            Image dimensions to use for the clipping of the polygon.
            If an ndarray, its shape will be used.
            If a tuple, it is assumed to represent the image shape and must
            contain at least two integers.

        Returns
        -------
        list of imgaug.Polygon
            Polygon, clipped to fall within the image dimensions.
            Returned as a list, because the clipping can split the polygon into
            multiple parts. The list may also be empty, if the polygon was
            fully outside of the image plane.

        """
        # load shapely lazily, which makes the dependency more optional
        import shapely.geometry

        # if fully out of image, clip everything away, nothing remaining
        if self.is_out_of_image(image, fully=True, partly=False):
            return []

        h, w = image.shape[0:2] if ia.is_np_array(image) else image[0:2]
        poly_shapely = self.to_shapely_polygon()
        poly_image = shapely.geometry.Polygon([(0, 0), (w, 0), (w, h), (0, h)])
        multipoly_inter_shapely = poly_shapely.intersection(poly_image)
        if not isinstance(multipoly_inter_shapely, shapely.geometry.MultiPolygon):
            ia.do_assert(isinstance(multipoly_inter_shapely, shapely.geometry.Polygon))
            multipoly_inter_shapely = shapely.geometry.MultiPolygon([multipoly_inter_shapely])

        polygons = []
        for poly_inter_shapely in multipoly_inter_shapely.geoms:
            polygons.append(Polygon.from_shapely(poly_inter_shapely, label=self.label))

        # shapely changes the order of points, we try here to preserve it as
        # much as possible
        polygons_reordered = []
        for polygon in polygons:
            found = False
            for x, y in self.exterior:
                closest_idx, dist = polygon.find_closest_point_index(x=x, y=y, return_distance=True)
                if dist < 1e-6:
                    polygon_reordered = polygon.change_first_point_by_index(closest_idx)
                    polygons_reordered.append(polygon_reordered)
                    found = True
                    break
            ia.do_assert(found)  # could only not find closest points if new polys are empty

        return polygons_reordered