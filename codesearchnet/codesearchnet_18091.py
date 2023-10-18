def _calc_loglikelihood(self, model=None, tile=None):
        """Allows for fast local updates of log-likelihood"""
        if model is None:
            res = self.residuals
        else:
            res = model - self._data[tile.slicer]

        sig, isig = self.sigma, 1.0/self.sigma
        nlogs = -np.log(np.sqrt(2*np.pi)*sig)*res.size
        return -0.5*isig*isig*np.dot(res.flat, res.flat) + nlogs