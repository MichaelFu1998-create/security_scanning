def predict(self, a, b):
        """ Compute the test statistic

        Args:
            a (array-like): Variable 1
            b (array-like): Variable 2

        Returns:
            float: test statistic
        """
        a = np.array(a).reshape((-1, 1))
        b = np.array(b).reshape((-1, 1))
        return (mutual_info_regression(a, b.reshape((-1,))) + mutual_info_regression(b, a.reshape((-1,))))/2