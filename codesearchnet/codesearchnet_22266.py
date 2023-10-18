def n_p(self):
        """
        The plasma density in SI units.
        """
        return 2*_sltr.GeV2joule(self.E)*_spc.epsilon_0 / (self.beta*_spc.elementary_charge)**2