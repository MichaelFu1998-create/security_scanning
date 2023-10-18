def nb0(self):
        """
        On-axis beam density :math:`n_{b,0}`.
        """
        return self.N_e / ( (2*_np.pi)**(3/2) * self.sig_r**2 * self.sig_xi)