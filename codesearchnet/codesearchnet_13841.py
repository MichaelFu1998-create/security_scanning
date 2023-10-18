def rect(self, x, y, width, height, roundness=0.0, draw=True, **kwargs):
        '''
        Draw a rectangle from x, y of width, height.

        :param startx: top left x-coordinate
        :param starty: top left y-coordinate

        :param width: height  Size of rectangle.
        :roundness: Corner roundness defaults to 0.0 (a right-angle).
        :draw: If True draws immediately.
        :fill: Optionally pass a fill color.

        :return: path representing the rectangle.

        '''
        path = self.BezierPath(**kwargs)
        path.rect(x, y, width, height, roundness, self.rectmode)
        if draw:
            path.draw()
        return path