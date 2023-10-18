def _segment_lengths(self, relative=False, n=20):
        """ Returns a list with the lengths of each segment in the path.
        """
        # From nodebox_gl
        lengths = []
        first = True
        for el in self._get_elements():
            if first is True:
                close_x, close_y = el.x, el.y
                first = False
            elif el.cmd == MOVETO:
                close_x, close_y = el.x, el.y
                lengths.append(0.0)
            elif el.cmd == CLOSE:
                lengths.append(self._linelength(x0, y0, close_x, close_y))
            elif el.cmd == LINETO:
                lengths.append(self._linelength(x0, y0, el.x, el.y))
            elif el.cmd == CURVETO:
                x3, y3, x1, y1, x2, y2 = el.x, el.y, el.c1x, el.c1y, el.c2x, el.c2y
                # (el.c1x, el.c1y, el.c2x, el.c2y, el.x, el.y)
                lengths.append(self._curvelength(x0, y0, x1, y1, x2, y2, x3, y3, n))
            if el.cmd != CLOSE:
                x0 = el.x
                y0 = el.y
        if relative:
            length = sum(lengths)
            try:
                # Relative segment lengths' sum is 1.0.
                return map(lambda l: l / length, lengths)
            except ZeroDivisionError:
                # If the length is zero, just return zero for all segments
                return [0.0] * len(lengths)
        else:
            return lengths