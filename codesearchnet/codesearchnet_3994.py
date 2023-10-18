def predict_proba(self, a, b, **kwargs):
        """Prediction method for pairwise causal inference using the ANM model.

        Args:
            a (numpy.ndarray): Variable 1
            b (numpy.ndarray): Variable 2

        Returns:
            float: Causation score (Value : 1 if a->b and -1 if b->a)
        """
        a = scale(a).reshape((-1, 1))
        b = scale(b).reshape((-1, 1))

        return self.anm_score(b, a) - self.anm_score(a, b)