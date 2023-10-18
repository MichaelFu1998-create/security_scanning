def nb0(self):
        """
        On-axis beam density :math:`n_{b,0}`.
        """
        return self.N_e / (4*_np.sqrt(3) * _np.pi * self.sig_x * self.sig_y * self.sig_xi)