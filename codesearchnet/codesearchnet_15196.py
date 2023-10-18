def gradient(self):
        r"""Gradient of the log of the marginal likelihood.

        Returns
        -------
        dict
            Map between variables to their gradient values.
        """
        self._update_approx()

        g = self._ep.lml_derivatives(self._X)
        ed = exp(-self.logitdelta)
        es = exp(self.logscale)

        grad = dict()
        grad["logitdelta"] = g["delta"] * (ed / (1 + ed)) / (1 + ed)
        grad["logscale"] = g["scale"] * es
        grad["beta"] = g["mean"]

        return grad