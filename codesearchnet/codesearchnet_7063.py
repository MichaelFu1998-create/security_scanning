def solve_T(self, P, V, quick=True):
        r'''Generic method to calculate `T` from a specified `P` and `V`.
        Provides SciPy's `newton` solver, and iterates to solve the general
        equation for `P`, recalculating `a_alpha` as a function of temperature
        using `a_alpha_and_derivatives` each iteration.

        Parameters
        ----------
        P : float
            Pressure, [Pa]
        V : float
            Molar volume, [m^3/mol]
        quick : bool, optional
            Unimplemented, although it may be possible to derive explicit 
            expressions as done for many pure-component EOS

        Returns
        -------
        T : float
            Temperature, [K]
        '''
        self.Tc = sum(self.Tcs)/self.N
        # -4 goes back from object, GCEOS
        return super(type(self).__mro__[-3], self).solve_T(P=P, V=V, quick=quick)