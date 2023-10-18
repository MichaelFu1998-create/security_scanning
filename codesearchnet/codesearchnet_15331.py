def bezier(self, points):
        """Draw a Bezier-curve.

        :param points: ex.) ((5, 5), (6, 6), (7, 7))
        :type points: list
        """
        coordinates = pgmagick.CoordinateList()
        for point in points:
            x, y = float(point[0]), float(point[1])
            coordinates.append(pgmagick.Coordinate(x, y))
        self.drawer.append(pgmagick.DrawableBezier(coordinates))