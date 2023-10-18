def _oldcall(self, rvecs):
        """Barnes w/o normalizing the weights"""
        g = self.filter_size

        dist0 = self._distance_matrix(self.x, self.x)
        dist1 = self._distance_matrix(rvecs, self.x)

        tmp = self._weight(dist0, g).dot(self.d)
        out = self._weight(dist1, g).dot(self.d)

        for i in range(self.iterations):
            out = out + self._weight(dist1, g).dot(self.d - tmp)
            tmp = tmp + self._weight(dist0, g).dot(self.d - tmp)
            g *= self.damp
        return out