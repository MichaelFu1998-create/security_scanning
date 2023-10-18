def circle(self, x, y, diameter, draw=True, **kwargs):
        '''Draw a circle
        :param x: x-coordinate of the top left corner
        :param y: y-coordinate of the top left corner
        :param diameter: Diameter of circle.
        :param draw: Draw immediately (defaults to True, set to False to inhibit drawing)
        :return: Path object representing circle
        '''
        return self.ellipse(x, y, diameter, diameter, draw, **kwargs)