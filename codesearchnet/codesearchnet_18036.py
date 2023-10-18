def _calc_lm_step(self, damped_JTJ, grad, subblock=None):
        """Calculates a Levenberg-Marquard step w/o acceleration"""
        delta0, res, rank, s = np.linalg.lstsq(damped_JTJ, -0.5*grad,
                rcond=self.min_eigval)
        if self._fresh_JTJ:
            CLOG.debug('%d degenerate of %d total directions' % (
                    delta0.size-rank, delta0.size))
        if subblock is not None:
            delta = np.zeros(self.J.shape[0])
            delta[subblock] = delta0
        else:
            delta = delta0.copy()
        return delta