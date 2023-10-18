def invert(self):
        """ Multiplying a matrix by its inverse produces the identity matrix.
        """
        m = self.matrix
        d = m[0] * m[4] - m[1] * m[3]
        self.matrix = [
             m[4] / d, -m[1] / d, 0,
             -m[3] / d,  m[0] / d, 0,
             (m[3] * m[7] - m[4] * m[6]) / d,
             -(m[0] * m[7] - m[1] * m[6]) / d,
             1
        ]