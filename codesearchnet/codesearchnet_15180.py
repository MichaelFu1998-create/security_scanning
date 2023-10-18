def B(self):
        """
        Effect-sizes parameter, B.
        """
        return unvec(self._vecB.value, (self.X.shape[1], self.A.shape[0]))