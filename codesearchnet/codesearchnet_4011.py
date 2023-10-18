def predict(self, a, b, sig=[-1, -1], maxpnt=500):
        """ Compute the test statistic

        Args:
            a (array-like): Variable 1
            b (array-like): Variable 2
            sig (list): [0] (resp [1]) is kernel size for a(resp b) (set to median distance if -1)
            maxpnt (int): maximum number of points used, for computational time

        Returns:
            float: test statistic
        """
        a = (a - np.mean(a)) / np.std(a)
        b = (b - np.mean(b)) / np.std(b)

        return FastHsicTestGamma(a, b, sig, maxpnt)