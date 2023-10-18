def calculate_integral(self, T1, T2):
        r'''Method to compute the enthalpy integral of heat capacity from 
        `T1` to `T2`. Analytically integrates across the piecewise spline
        as necessary.
            
        Parameters
        ----------
        T1 : float
            Initial temperature, [K]
        T2 : float
            Final temperature, [K]
            
        Returns
        -------
        dS : float
            Enthalpy difference between `T1` and `T2`, [J/mol/K]
        '''        
        # Simplify the problem so we can assume T2 >= T1
        if T2 < T1:
            flipped = True
            T1, T2 = T2, T1
        else:
            flipped = False
        
        # Fastest case - only one coefficient set, occurs surprisingly often
        if self.n == 1:
            dH = (Zabransky_cubic_integral(T2, *self.coeff_sets[0])
                  - Zabransky_cubic_integral(T1, *self.coeff_sets[0]))
        else:
            ind_T1, ind_T2 = self._coeff_ind_from_T(T1), self._coeff_ind_from_T(T2)
            # Second fastest case - both are in the same coefficient set
            if ind_T1 == ind_T2:
                dH = (Zabransky_cubic_integral(T2, *self.coeff_sets[ind_T2])
                        - Zabransky_cubic_integral(T1, *self.coeff_sets[ind_T1]))
            # Fo through the loop if we need to - inevitably slow 
            else:
                dH = (Zabransky_cubic_integral(self.Ts[ind_T1], *self.coeff_sets[ind_T1])
                      - Zabransky_cubic_integral(T1, *self.coeff_sets[ind_T1]))
                for i in range(ind_T1, ind_T2):
                    diff =(Zabransky_cubic_integral(self.Ts[i+1], *self.coeff_sets[i])
                          - Zabransky_cubic_integral(self.Ts[i], *self.coeff_sets[i]))
                    dH += diff
                end = (Zabransky_cubic_integral(T2, *self.coeff_sets[ind_T2])
                      - Zabransky_cubic_integral(self.Ts[ind_T2], *self.coeff_sets[ind_T2]))
                dH += end
        return -dH if flipped else dH