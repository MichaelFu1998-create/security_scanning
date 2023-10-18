def to_shapely_polygon(self):
        """
        Convert this polygon to a Shapely polygon.

        Returns
        -------
        shapely.geometry.Polygon
            The Shapely polygon matching this polygon's exterior.

        """
        # load shapely lazily, which makes the dependency more optional
        import shapely.geometry

        return shapely.geometry.Polygon([(point[0], point[1]) for point in self.exterior])