def point(self, t, segments=None):
        """
            Returns the PathElement at time t (0.0-1.0) on the path.

            Returns coordinates for point at t on the path.
            Gets the length of the path, based on the length of each curve and line in the path.
            Determines in what segment t falls. Gets the point on that segment.
            When you supply the list of segment lengths yourself, as returned from length(path, segmented=True),
            point() works about thirty times faster in a for-loop since it doesn't need to recalculate
            the length during each iteration.
        """
        # Originally from nodebox-gl
        if len(self._elements) == 0:
            raise PathError("The given path is empty")

        if self._segments is None:
            self._segments = self._get_length(segmented=True, precision=10)

        i, t, closeto = self._locate(t, segments=self._segments)
        x0, y0 = self[i].x, self[i].y
        p1 = self[i + 1]
        if p1.cmd == CLOSE:
            x, y = self._linepoint(t, x0, y0, closeto.x, closeto.y)
            return PathElement(LINETO, x, y)
        elif p1.cmd in (LINETO, MOVETO):
            x1, y1 = p1.x, p1.y
            x, y = self._linepoint(t, x0, y0, x1, y1)
            return PathElement(LINETO, x, y)
        elif p1.cmd == CURVETO:
            # Note: the handles need to be interpreted differenty than in a BezierPath.
            # In a BezierPath, ctrl1 is how the curve started, and ctrl2 how it arrives in this point.
            # Here, ctrl1 is how the curve arrives, and ctrl2 how it continues to the next point.
            x3, y3, x1, y1, x2, y2 = p1.x, p1.y, p1.ctrl1.x, p1.ctrl1.y, p1.ctrl2.x, p1.ctrl2.y
            x, y, c1x, c1y, c2x, c2y = self._curvepoint(t, x0, y0, x1, y1, x2, y2, x3, y3)
            return PathElement(CURVETO, c1x, c1y, c2x, c2y, x, y)
        else:
            raise PathError("Unknown cmd '%s' for p1 %s" % (p1.cmd, p1))