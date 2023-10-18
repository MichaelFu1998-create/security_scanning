def predict(self, a, b, **kwargs):
        """Perform the independence test.

        :param a: input data
        :param b: input data
        :type a: array-like, numerical data
        :type b: array-like, numerical data
        :return: dependency statistic (1=Highly dependent, 0=Not dependent)
        :rtype: float
        """
        binning_alg = kwargs.get('bins', 'fd')
        return metrics.adjusted_mutual_info_score(bin_variable(a, bins=binning_alg),
                                                  bin_variable(b, bins=binning_alg))