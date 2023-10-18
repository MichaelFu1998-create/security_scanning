def solve_T(self, P, V, quick=True):
        '''Generic method to calculate `T` from a specified `P` and `V`.
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
            Whether to use a SymPy cse-derived expression (3x faster) or 
            individual formulas - not applicable where a numerical solver is
            used.

        Returns
        -------
        T : float
            Temperature, [K]
        '''
        def to_solve(T):
            a_alpha = self.a_alpha_and_derivatives(T, full=False)
            P_calc = R*T/(V-self.b) - a_alpha/(V*V + self.delta*V + self.epsilon)
            return P_calc - P
        return newton(to_solve, self.Tc*0.5)