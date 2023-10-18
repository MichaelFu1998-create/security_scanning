def _eval_firstorder(self, rvecs, data, sigma):
        """The first-order Barnes approximation"""
        if not self.blocksize:
            dist_between_points = self._distance_matrix(rvecs, self.x)
            gaussian_weights = self._weight(dist_between_points, sigma=sigma)
            return gaussian_weights.dot(data) / gaussian_weights.sum(axis=1)
        else:
            # Now rather than calculating the distance matrix all at once,
            # we do it in chunks over rvecs
            ans = np.zeros(rvecs.shape[0], dtype='float')
            bs = self.blocksize
            for a in range(0, rvecs.shape[0], bs):
                dist = self._distance_matrix(rvecs[a:a+bs], self.x)
                weights = self._weight(dist, sigma=sigma)
                ans[a:a+bs] += weights.dot(data) / weights.sum(axis=1)
            return ans