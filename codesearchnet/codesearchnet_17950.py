def update(self, params, values):
        """Calls an update, but clips radii to be > 0"""
        # radparams = self.param_radii()
        params = listify(params)
        values = listify(values)
        for i, p in enumerate(params):
            # if (p in radparams) & (values[i] < 0):
            if (p[-2:] == '-a') and (values[i] < 0):
                values[i] = 0.0
        super(PlatonicSpheresCollection, self).update(params, values)