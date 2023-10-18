def angle(self, x0, y0, x1, y1):
        
        """ Calculates the angle between two points.
        """
    
        a = degrees( atan((y1-y0) / (x1-x0+0.00001)) ) + 360
        if x1-x0 < 0: a += 180
        return a