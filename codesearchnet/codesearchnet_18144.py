def characterize_psf(self):
        """ Get support size and drift polynomial for current set of params """
        # there may be an issue with the support and characterization--
        # it might be best to do the characterization with the same support
        # as the calculated psf.
        l,u = max(self.zrange[0], self.param_dict['psf-zslab']), self.zrange[1]

        size_l, drift_l = self.measure_size_drift(l)
        size_u, drift_u = self.measure_size_drift(u)

        # must be odd for now or have a better system for getting the center
        self.support = util.oddify(2*self.support_factor*size_u.astype('int'))
        self.drift_poly = np.polyfit([l, u], [drift_l, drift_u], 1)

        if self.cutoffval is not None:
            psf, vec, size_l = self.psf_slice(l, size=51, zoffset=drift_l, getextent=True)
            psf, vec, size_u = self.psf_slice(u, size=51, zoffset=drift_u, getextent=True)

            ss = [np.abs(i).sum(axis=-1) for i in [size_l, size_u]]
            self.support = util.oddify(util.amax(*ss))