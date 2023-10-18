def _c2x(self, c):
        """ Convert cheb coordinates to windowdow coordinates """
        return 0.5 * (self.window[0] + self.window[1] +
                      c * (self.window[1] - self.window[0]))