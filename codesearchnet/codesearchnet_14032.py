def contains_point(self, x, y, d=2):
        
        """ Returns true when x, y is on the path stroke outline.
        """
        
        if self.path != None and len(self.path) > 1 \
        and self.path.contains(x, y):
            # If all points around the mouse are also part of the path,
            # this means we are somewhere INSIDE the path.
            # Only points near the edge (i.e. on the outline stroke)
            # should propagate.
            if not self.path.contains(x+d, y) \
            or not self.path.contains(x, y+d) \
            or not self.path.contains(x-d, y) \
            or not self.path.contains(x, y-d) \
            or not self.path.contains(x+d, y+d) \
            or not self.path.contains(x-d, y-d) \
            or not self.path.contains(x+d, y-d) \
            or not self.path.contains(x-d, y+d):
                return True

        return False