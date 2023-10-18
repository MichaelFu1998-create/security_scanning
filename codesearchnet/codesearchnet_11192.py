def fbeta_score(self, beta=1.0):
        r"""Return :math:`F_{\beta}` score.

        :math:`F_{\beta}` for a positive real value :math:`\beta` "measures
        the effectiveness of retrieval with respect to a user who
        attaches :math:`\beta` times as much importance to recall as
        precision" (van Rijsbergen 1979)

        :math:`F_{\beta}` score is defined as:
        :math:`(1 + \beta^2) \cdot \frac{precision \cdot recall}
        {((\beta^2 \cdot precision) + recall)}`

        Cf. https://en.wikipedia.org/wiki/F1_score

        Parameters
        ----------
        beta : float
            The :math:`\beta` parameter in the above formula

        Returns
        -------
        float
            The :math:`F_{\beta}` of the confusion table

        Raises
        ------
        AttributeError
            Beta must be a positive real value

        Examples
        --------
        >>> ct = ConfusionTable(120, 60, 20, 30)
        >>> ct.fbeta_score()
        0.8275862068965518
        >>> ct.fbeta_score(beta=0.1)
        0.8565371024734982

        """
        if beta <= 0:
            raise AttributeError('Beta must be a positive real value.')
        precision = self.precision()
        recall = self.recall()
        return (
            (1 + beta ** 2)
            * precision
            * recall
            / ((beta ** 2 * precision) + recall)
        )