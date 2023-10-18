def line(self, x1, y1, x2, y2, draw=True):
        '''Draws a line from (x1,y1) to (x2,y2)'''
        p = self._path
        self.newpath()
        self.moveto(x1,y1)
        self.lineto(x2,y2)
        self.endpath(draw=draw)
        self._path = p
        return p