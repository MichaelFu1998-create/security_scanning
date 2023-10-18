def to_polygon(self):
        """
        Generate a polygon from the line string points.

        Returns
        -------
        imgaug.augmentables.polys.Polygon
            Polygon with the same corner points as the line string.
            Note that the polygon might be invalid, e.g. contain less than 3
            points or have self-intersections.

        """
        from .polys import Polygon
        return Polygon(self.coords, label=self.label)