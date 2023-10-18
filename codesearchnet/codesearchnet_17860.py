def _x2c(self, x):
        """ Convert windowdow coordinates to cheb coordinates [-1,1] """
        return ((2 * x - self.window[1] - self.window[0]) /
                (self.window[1] - self.window[0]))