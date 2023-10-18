def _curvepoint(self, t, x0, y0, x1, y1, x2, y2, x3, y3, handles=False):
        """ Returns coordinates for point at t on the spline.
            Calculates the coordinates of x and y for a point at t on the cubic bezier spline,
            and its control points, based on the de Casteljau interpolation algorithm.
            The t parameter is a number between 0.0 and 1.0,
            x0 and y0 define the starting point of the spline,
            x1 and y1 its control point,
            x3 and y3 the ending point of the spline,
            x2 and y2 its control point.
            If the handles parameter is set, returns not only the point at t,
            but the modified control points of p0 and p3 should this point split the path as well.
        """
        # Originally from nodebox-gl
        mint = 1 - t
        x01 = x0 * mint + x1 * t
        y01 = y0 * mint + y1 * t
        x12 = x1 * mint + x2 * t
        y12 = y1 * mint + y2 * t
        x23 = x2 * mint + x3 * t
        y23 = y2 * mint + y3 * t
        out_c1x = x01 * mint + x12 * t
        out_c1y = y01 * mint + y12 * t
        out_c2x = x12 * mint + x23 * t
        out_c2y = y12 * mint + y23 * t
        out_x = out_c1x * mint + out_c2x * t
        out_y = out_c1y * mint + out_c2y * t
        if not handles:
            return (out_x, out_y, out_c1x, out_c1y, out_c2x, out_c2y)
        else:
            return (out_x, out_y, out_c1x, out_c1y, out_c2x, out_c2y, x01, y01, x23, y23)