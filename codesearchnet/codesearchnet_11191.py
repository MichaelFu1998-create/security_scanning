def pr_lmean(self):
        r"""Return logarithmic mean of precision & recall.

        The logarithmic mean is:
        0 if either precision or recall is 0,
        the precision if they are equal,
        otherwise :math:`\frac{precision - recall}
        {ln(precision) - ln(recall)}`

        Cf. https://en.wikipedia.org/wiki/Logarithmic_mean

        Returns
        -------
        float
            The logarithmic mean of the confusion table's precision & recall

        Example
        -------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.pr_lmean()
        0.8282429171492667

        """
        precision = self.precision()
        recall = self.recall()
        if not precision or not recall:
            return 0.0
        elif precision == recall:
            return precision
        return (precision - recall) / (math.log(precision) - math.log(recall))