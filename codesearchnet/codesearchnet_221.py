def from_shapely(polygon_shapely, label=None):
        """
        Create a polygon from a Shapely polygon.

        Note: This will remove any holes in the Shapely polygon.

        Parameters
        ----------
        polygon_shapely : shapely.geometry.Polygon
             The shapely polygon.

        label : None or str, optional
            The label of the new polygon.

        Returns
        -------
        imgaug.Polygon
            A polygon with the same exterior as the Shapely polygon.

        """
        # load shapely lazily, which makes the dependency more optional
        import shapely.geometry

        ia.do_assert(isinstance(polygon_shapely, shapely.geometry.Polygon))
        # polygon_shapely.exterior can be None if the polygon was instantiated without points
        if polygon_shapely.exterior is None or len(polygon_shapely.exterior.coords) == 0:
            return Polygon([], label=label)
        exterior = np.float32([[x, y] for (x, y) in polygon_shapely.exterior.coords])
        return Polygon(exterior, label=label)