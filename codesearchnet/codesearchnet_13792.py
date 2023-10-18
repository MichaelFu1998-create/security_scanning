def _darkest(self):
        
        """ Returns the darkest swatch.
        
        Knowing the contract between a light and a dark swatch
        can help us decide how to display readable typography.
        
        """
        
        rgb, n = (1.0, 1.0, 1.0), 3.0
        for r,g,b in self:
            if r+g+b < n:
                rgb, n = (r,g,b), r+g+b
        
        return rgb