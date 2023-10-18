def _draw(self):
        """ Interal draw method, simply prints to screen """
        if self.display:
            print(self._formatstr.format(**self.__dict__), end='')
            sys.stdout.flush()