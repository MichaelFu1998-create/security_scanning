def scale(self, x=1, y=None):
        '''
        Set a scale at which to draw objects.

        1.0 draws objects at their natural size

        :param x: Scale on the horizontal plane
        :param y: Scale on the vertical plane
        '''
        if not y:
            y = x
        if x == 0:
            # Cairo borks on zero values
            x = 1
        if y == 0:
            y = 1
        self._canvas.scale(x, y)