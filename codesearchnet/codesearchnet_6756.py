def Psat(self, T, polish=False):
        r'''Generic method to calculate vapor pressure for a specified `T`.
        
        From Tc to 0.32Tc, uses a 10th order polynomial of the following form:
        
        .. math::
            \ln\frac{P_r}{T_r} = \sum_{k=0}^{10} C_k\left(\frac{\alpha}{T_r}
            -1\right)^{k}
                    
        If `polish` is True, SciPy's `newton` solver is launched with the 
        calculated vapor pressure as an initial guess in an attempt to get more
        accuracy. This may not converge however.
        
        Results above the critical temperature are meaningless. A first-order 
        polynomial is used to extrapolate under 0.32 Tc; however, there is 
        normally not a volume solution to the EOS which can produce that
        low of a pressure.
        
        Parameters
        ----------
        T : float
            Temperature, [K]
        polish : bool, optional
            Whether to attempt to use a numerical solver to make the solution
            more precise or not

        Returns
        -------
        Psat : float
            Vapor pressure, [Pa]
            
        Notes
        -----
        EOSs sharing the same `b`, `delta`, and `epsilon` have the same
        coefficient sets.
        
        All coefficients were derived with numpy's polyfit. The intersection
        between the polynomials is continuous, but there is a step change
        in its derivative.
        
        Form for the regression is inspired from [1]_.
                    
        References
        ----------
        .. [1] Soave, G. "Direct Calculation of Pure-Compound Vapour Pressures 
           through Cubic Equations of State." Fluid Phase Equilibria 31, no. 2 
           (January 1, 1986): 203-7. doi:10.1016/0378-3812(86)90013-0. 
        '''
        alpha = self.a_alpha_and_derivatives(T, full=False)/self.a
        Tr = T/self.Tc
        x = alpha/Tr - 1.
        c = self.Psat_coeffs_limiting if Tr < 0.32 else self.Psat_coeffs
        y = horner(c, x)
        try:
            Psat = exp(y)*Tr*self.Pc
        except OverflowError:
            # coefficients sometimes overflow before T is lowered to 0.32Tr
            polish = False
            Psat = 0
        
        if polish:
            def to_solve(P):
                # For use by newton. Only supports initialization with Tc, Pc and omega
                # ~200x slower and not guaranteed to converge
                e = self.__class__(Tc=self.Tc, Pc=self.Pc, omega=self.omega, T=T, P=P)
                err = e.fugacity_l - e.fugacity_g
                return err
            Psat = newton(to_solve, Psat)
        return Psat