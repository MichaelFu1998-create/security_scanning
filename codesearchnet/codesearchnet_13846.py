def star(self, startx, starty, points=20, outer=100, inner=50, draw=True, **kwargs):
        '''Draws a star.
        '''
        # Taken from Nodebox.
        self.beginpath(**kwargs)
        self.moveto(startx, starty + outer)

        for i in range(1, int(2 * points)):
            angle = i * pi / points
            x = sin(angle)
            y = cos(angle)
            if i % 2:
                radius = inner
            else:
                radius = outer
            x = startx + radius * x
            y = starty + radius * y
            self.lineto(x, y)

        return self.endpath(draw)