def _newcall(self, rvecs):
        """Correct, normalized version of Barnes"""
        # 1. Initial guess for output:
        sigma = 1*self.filter_size
        out = self._eval_firstorder(rvecs, self.d, sigma)
        # 2. There are differences between 0th order at the points and
        #    the passed data, so we iterate to remove:
        ondata = self._eval_firstorder(self.x, self.d, sigma)
        for i in range(self.iterations):
            out += self._eval_firstorder(rvecs, self.d-ondata, sigma)
            ondata += self._eval_firstorder(self.x, self.d-ondata, sigma)
            sigma *= self.damp
        return out