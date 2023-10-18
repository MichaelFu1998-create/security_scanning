def predict_proba(self, a, b, idx=0, **kwargs):
        """ Use Jarfo to predict the causal direction of a pair of vars.

        Args:
            a (numpy.ndarray): Variable 1
            b (numpy.ndarray): Variable 2
            idx (int): (optional) index number for printing purposes

        Returns:
            float: Causation score (Value : 1 if a->b and -1 if b->a)
        """
        return self.predict_dataset(DataFrame([[a, b]],
                                              columns=['A', 'B']))