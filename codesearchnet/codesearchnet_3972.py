def featurize_row(self, x, y):
        """ Projects the causal pair to the RKHS using the sampled kernel approximation.

        Args:
            x (np.ndarray): Variable 1
            y (np.ndarray): Variable 2

        Returns:
            np.ndarray: projected empirical distributions into a single fixed-size vector.
        """
        x = x.ravel()
        y = y.ravel()
        b = np.ones(x.shape)
        dx = np.cos(np.dot(self.W2, np.vstack((x, b)))).mean(1)
        dy = np.cos(np.dot(self.W2, np.vstack((y, b)))).mean(1)
        if(sum(dx) > sum(dy)):
            return np.hstack((dx, dy,
                              np.cos(np.dot(self.W, np.vstack((x, y, b)))).mean(1)))
        else:
            return np.hstack((dx, dy,
                              np.cos(np.dot(self.W, np.vstack((y, x, b)))).mean(1)))