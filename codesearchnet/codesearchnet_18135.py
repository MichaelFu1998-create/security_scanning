def randomize_parameters(self, ptp=0.2, fourier=False, vmin=None, vmax=None):
        """
        Create random parameters for this ILM that mimic experiments
        as closely as possible without real assumptions.
        """
        if vmin is not None and vmax is not None:
            ptp = vmax - vmin
        elif vmax is not None and vmin is None:
            vmin = vmax - ptp
        elif vmin is not None and vmax is None:
            vmax = vmin + ptp
        else:
            vmax = 1.0
            vmin = vmax - ptp

        self.set_values(self.category+'-scale', 1.0)
        self.set_values(self.category+'-off', 0.0)

        for k, v in iteritems(self.poly_params):
            norm = (self.zorder + 1.0)*2
            self.set_values(k, ptp*(np.random.rand() - 0.5) / norm)

        for i, p in enumerate(self.barnes_params):
            N = len(p)
            if fourier:
                t = ((np.random.rand(N)-0.5) + 1.j*(np.random.rand(N)-0.5))/(np.arange(N)+1)
                q = np.real(np.fft.ifftn(t)) / (i+1)
            else:
                t = ptp*np.sqrt(N)*(np.random.rand(N)-0.5)
                q = np.cumsum(t) / (i+1)

            q = ptp * q / q.ptp() / len(self.barnes_params)
            q -= q.mean()
            self.set_values(p, q)

        self._norm_stat = [ptp, vmin]

        if self.shape:
            self.initialize()

        if self._parent:
            param = self.category+'-scale'
            self.trigger_update(param, self.get_values(param))