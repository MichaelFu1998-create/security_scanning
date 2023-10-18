def reflect(self, x0, y0, x, y):
        
        """ Reflects the point x, y through origin x0, y0.
        """
                
        rx = x0 - (x-x0)
        ry = y0 - (y-y0)
        return rx, ry