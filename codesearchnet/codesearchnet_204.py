def area(self):
        """
        Estimate the area of the polygon.

        Returns
        -------
        number
            Area of the polygon.

        """
        if len(self.exterior) < 3:
            raise Exception("Cannot compute the polygon's area because it contains less than three points.")
        poly = self.to_shapely_polygon()
        return poly.area