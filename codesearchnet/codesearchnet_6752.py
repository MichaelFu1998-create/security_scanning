def set_from_PT(self, Vs):
        '''Counts the number of real volumes in `Vs`, and determines what to do.
        If there is only one real volume, the method 
        `set_properties_from_solution` is called with it. If there are
        two real volumes, `set_properties_from_solution` is called once with  
        each volume. The phase is returned by `set_properties_from_solution`, 
        and the volumes is set to either `V_l` or `V_g` as appropriate. 

        Parameters
        ----------
        Vs : list[float]
            Three possible molar volumes, [m^3/mol]
        '''
        # All roots will have some imaginary component; ignore them if > 1E-9
        good_roots = []
        bad_roots = []
        for i in Vs:
            j = i.real
            if abs(i.imag) > 1E-9 or j < 0:
                bad_roots.append(i)
            else:
                good_roots.append(j)
                
        if len(bad_roots) == 2: 
            V = good_roots[0]
            self.phase = self.set_properties_from_solution(self.T, self.P, V, self.b, self.delta, self.epsilon, self.a_alpha, self.da_alpha_dT, self.d2a_alpha_dT2)
            if self.phase == 'l':
                self.V_l = V
            else:
                self.V_g = V
        else:
            # Even in the case of three real roots, it is still the min/max that make sense
            self.V_l, self.V_g = min(good_roots), max(good_roots)
            [self.set_properties_from_solution(self.T, self.P, V, self.b, self.delta, self.epsilon, self.a_alpha, self.da_alpha_dT, self.d2a_alpha_dT2) for V in [self.V_l, self.V_g]]
            self.phase = 'l/g'