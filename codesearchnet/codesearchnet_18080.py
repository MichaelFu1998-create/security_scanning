def _grad(self, funct, params=None, dl=2e-5, rts=False, nout=1, out=None,
            **kwargs):
        """
        Gradient of `func` wrt a set of parameters params. (see _graddoc)
        """
        if params is None:
            params = self.param_all()

        ps = util.listify(params)
        f0 = funct(**kwargs)

        # get the shape of the entire gradient to return and make an array
        calc_shape = (
                lambda ar: (len(ps),) + (ar.shape if isinstance(
                ar, np.ndarray) else (1,)))
        if out is not None:
            grad = out  # reference
        elif nout == 1:
            shape = calc_shape(f0)
            grad = np.zeros(shape)  # must be preallocated for mem reasons
        else:
            shape = [calc_shape(f0[i]) for i in range(nout)]
            grad = [np.zeros(shp) for shp in shape]

        for i, p in enumerate(ps):
            if nout == 1:
                grad[i] = self._grad_one_param(funct, p, dl=dl, rts=rts,
                        nout=nout, **kwargs)
            else:
                stuff = self._grad_one_param(funct, p, dl=dl, rts=rts,
                        nout=nout, **kwargs)
                for a in range(nout): grad[a][i] = stuff[a]
        return grad