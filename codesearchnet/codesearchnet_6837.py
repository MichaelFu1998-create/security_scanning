def estimate(self):
        '''Method to compute all available properties with the Joback method;
        returns their results as a dict. For the tempearture dependent values
        Cpig and mul, both the coefficients and objects to perform calculations
        are returned.
        '''
        # Pre-generate the coefficients or they will not be returned
        self.mul(300)
        self.Cpig(300) 
        estimates = {'Tb': self.Tb(self.counts),
                     'Tm': self.Tm(self.counts),
                     'Tc': self.Tc(self.counts, self.Tb_estimated),
                     'Pc': self.Pc(self.counts, self.atom_count),
                     'Vc': self.Vc(self.counts),
                     'Hf': self.Hf(self.counts),
                     'Gf': self.Gf(self.counts),
                     'Hfus': self.Hfus(self.counts),
                     'Hvap': self.Hvap(self.counts),
                     'mul': self.mul,
                     'mul_coeffs': self.calculated_mul_coeffs,
                     'Cpig': self.Cpig,
                     'Cpig_coeffs': self.calculated_Cpig_coeffs}
        return estimates