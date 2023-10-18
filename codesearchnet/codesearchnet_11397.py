def line(self, p1, p2, resolution=1):
        """Resolve the points to make a line between two points."""
        xdiff = max(p1.x, p2.x) - min(p1.x, p2.x)
        ydiff = max(p1.y, p2.y) - min(p1.y, p2.y)
        xdir = [-1, 1][int(p1.x <= p2.x)]
        ydir = [-1, 1][int(p1.y <= p2.y)]
        r = int(round(max(xdiff, ydiff)))
        if r == 0:
            return

        for i in range((r + 1) * resolution):
            x = p1.x
            y = p1.y

            if xdiff:
                x += (float(i) * xdiff) / r * xdir / resolution
            if ydiff:
                y += (float(i) * ydiff) / r * ydir / resolution

            yield Point((x, y))