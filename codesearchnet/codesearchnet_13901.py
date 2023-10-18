def transform_point(self, x, y):
        """ Returns the new coordinates of (x,y) after transformation.
        """
        m = self.matrix
        return (x*m[0]+y*m[3]+m[6], x*m[1]+y*m[4]+m[7])