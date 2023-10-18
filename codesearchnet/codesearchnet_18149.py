def characterize_psf(self):
        """ Get support size and drift polynomial for current set of params """
        l,u = max(self.zrange[0], self.param_dict['psf-zslab']), self.zrange[1]

        size_l, drift_l = self.measure_size_drift(l, size=self.support)
        size_u, drift_u = self.measure_size_drift(u, size=self.support)

        self.drift_poly = np.polyfit([l, u], [drift_l, drift_u], 1)