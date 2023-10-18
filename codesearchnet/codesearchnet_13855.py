def fill(self, *args):
        '''Sets a fill color, applying it to new paths.

        :param args: color in supported format
        '''
        if args is not None:
            self._canvas.fillcolor = self.color(*args)
        return self._canvas.fillcolor