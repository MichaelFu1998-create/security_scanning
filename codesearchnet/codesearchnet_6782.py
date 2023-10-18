def solve_T(self, P, V, quick=True):
        r'''Method to calculate `T` from a specified `P` and `V` for the API 
        SRK EOS. Uses `a`, `b`, and `Tc` obtained from the class's namespace.

        Parameters
        ----------
        P : float
            Pressure, [Pa]
        V : float
            Molar volume, [m^3/mol]
        quick : bool, optional
            Whether to use a SymPy cse-derived expression (3x faster) or 
            individual formulas

        Returns
        -------
        T : float
            Temperature, [K]

        Notes
        -----
        If S2 is set to 0, the solution is the same as in the SRK EOS, and that
        is used. Otherwise, newton's method must be used to solve for `T`. 
        There are 8 roots of T in that case, six of them real. No guarantee can
        be made regarding which root will be obtained.
        '''
        if self.S2 == 0:
            self.m = self.S1
            return SRK.solve_T(self, P, V, quick=quick)
        else:
            # Previously coded method is  63 microseconds vs 47 here
#            return super(SRK, self).solve_T(P, V, quick=quick) 
            Tc, a, b, S1, S2 = self.Tc, self.a, self.b, self.S1, self.S2
            if quick:
                x2 = R/(V-b)
                x3 = (V*(V + b))
                def to_solve(T):
                    x0 = (T/Tc)**0.5
                    x1 = x0 - 1.
                    return (x2*T - a*(S1*x1 + S2*x1/x0 - 1.)**2/x3) - P
            else:
                def to_solve(T):
                    P_calc = R*T/(V - b) - a*(S1*(-sqrt(T/Tc) + 1) + S2*(-sqrt(T/Tc) + 1)/sqrt(T/Tc) + 1)**2/(V*(V + b))
                    return P_calc - P
            return newton(to_solve, Tc*0.5)