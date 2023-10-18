def coordinates(self, x0, y0, distance, angle):
        
        """ Calculates the coordinates of a point from the origin.
        """
        
        x = x0 + cos(radians(angle)) * distance
        y = y0 + sin(radians(angle)) * distance
        return Point(x, y)