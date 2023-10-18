def stroke(self, *args):
        '''Set a stroke color, applying it to new paths.

        :param args: color in supported format
        '''
        if args is not None:
            self._canvas.strokecolor = self.color(*args)
        return self._canvas.strokecolor