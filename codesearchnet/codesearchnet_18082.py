def _hess(self, funct, params=None, dl=2e-5, rts=False, **kwargs):
        """
        Hessian of a `func` wrt to parmaeters `params`. (see _graddoc)
        """
        if params is None:
            params = self.param_all()

        ps = util.listify(params)
        f0 = funct(**kwargs)

        # get the shape of the entire hessian, allocate an array
        shape = f0.shape if isinstance(f0, np.ndarray) else (1,)
        shape = (len(ps), len(ps)) + shape
        hess = np.zeros(shape)

        for i, pi in enumerate(ps):
            for j, pj in enumerate(ps[i:]):
                J = j + i
                thess = self._hess_two_param(funct, pi, pj, dl=dl, rts=rts, **kwargs)
                hess[i][J] = thess
                hess[J][i] = thess
        return np.squeeze(hess)