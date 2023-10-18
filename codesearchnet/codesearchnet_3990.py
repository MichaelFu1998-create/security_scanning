def predict_proba(self, a, b, **kwargs):
        """ Infer causal relationships between 2 variables using the RECI statistic

        :param a: Input variable 1
        :param b: Input variable 2
        :return: Causation coefficient (Value : 1 if a->b and -1 if b->a)
        :rtype: float
        """
        return self.b_fit_score(b, a) - self.b_fit_score(a, b)