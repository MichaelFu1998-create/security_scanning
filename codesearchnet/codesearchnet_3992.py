def predict_proba(self, a, b, **kwargs):
        """ Infer causal relationships between 2 variables using the CDS statistic

        Args:
            a (numpy.ndarray): Variable 1
            b (numpy.ndarray): Variable 2

        Returns:
            float: Causation score (Value : 1 if a->b and -1 if b->a)
        """
        return self.cds_score(b, a) - self.cds_score(a, b)