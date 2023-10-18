def get_intersections(self):
        """
        Return a list of unordered intersection points.
        """
        if Real is float:
            return list(self.intersections.keys())
        else:
            return [(float(p[0]), float(p[1])) for p in self.intersections.keys()]