def add_coeffs(self, Tmin, Tmax, coeffs):
        '''Called internally during the parsing of the Zabransky database, to
        add coefficients as they are read one per line'''
        self.n += 1
        if not self.Ts:
            self.Ts = [Tmin, Tmax]
            self.coeff_sets = [coeffs]
        else:
            for ind, T in enumerate(self.Ts):
                if Tmin < T:
                    # Under an existing coefficient set - assume Tmax will come from another set
                    self.Ts.insert(ind, Tmin) 
                    self.coeff_sets.insert(ind, coeffs)
                    return
            # Must be appended to end instead
            self.Ts.append(Tmax)
            self.coeff_sets.append(coeffs)