def _jtj(self, funct, params=None, dl=2e-5, rts=False, **kwargs):
        """
        jTj of a `func` wrt to parmaeters `params`. (see _graddoc)
        """
        grad = self._grad(funct=funct, params=params, dl=dl, rts=rts, **kwargs)
        return np.dot(grad, grad.T)