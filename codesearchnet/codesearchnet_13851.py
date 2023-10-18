def findpath(self, points, curvature=1.0):

        """Constructs a path between the given list of points.

        Interpolates the list of points and determines
        a smooth bezier path betweem them.

        The curvature parameter offers some control on
        how separate segments are stitched together:
        from straight angles to smooth curves.
        Curvature is only useful if the path has more than  three points.
        """

        # The list of points consists of Point objects,
        # but it shouldn't crash on something straightforward
        # as someone supplying a list of (x,y)-tuples.

        for i, pt in enumerate(points):
            if type(pt) == TupleType:
                points[i] = Point(pt[0], pt[1])

        if len(points) == 0:
            return None
        if len(points) == 1:
            path = self.BezierPath(None)
            path.moveto(points[0].x, points[0].y)
            return path
        if len(points) == 2:
            path = self.BezierPath(None)
            path.moveto(points[0].x, points[0].y)
            path.lineto(points[1].x, points[1].y)
            return path

        # Zero curvature means straight lines.

        curvature = max(0, min(1, curvature))
        if curvature == 0:
            path = self.BezierPath(None)
            path.moveto(points[0].x, points[0].y)
            for i in range(len(points)):
                path.lineto(points[i].x, points[i].y)
            return path

        curvature = 4 + (1.0 - curvature) * 40

        dx = {0: 0, len(points) - 1: 0}
        dy = {0: 0, len(points) - 1: 0}
        bi = {1: -0.25}
        ax = {1: (points[2].x - points[0].x - dx[0]) / 4}
        ay = {1: (points[2].y - points[0].y - dy[0]) / 4}

        for i in range(2, len(points) - 1):
            bi[i] = -1 / (curvature + bi[i - 1])
            ax[i] = -(points[i + 1].x - points[i - 1].x - ax[i - 1]) * bi[i]
            ay[i] = -(points[i + 1].y - points[i - 1].y - ay[i - 1]) * bi[i]

        r = range(1, len(points) - 1)
        r.reverse()
        for i in r:
            dx[i] = ax[i] + dx[i + 1] * bi[i]
            dy[i] = ay[i] + dy[i + 1] * bi[i]

        path = self.BezierPath(None)
        path.moveto(points[0].x, points[0].y)
        for i in range(len(points) - 1):
            path.curveto(points[i].x + dx[i],
                         points[i].y + dy[i],
                         points[i + 1].x - dx[i + 1],
                         points[i + 1].y - dy[i + 1],
                         points[i + 1].x,
                         points[i + 1].y)

        return path