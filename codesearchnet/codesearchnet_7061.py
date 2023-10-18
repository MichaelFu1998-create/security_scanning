def a_alpha_and_derivatives(self, T, full=True, quick=True):
        r'''Method to calculate `a_alpha` and its first and second
        derivatives for an EOS with the Van der Waals mixing rules. Uses the
        parent class's interface to compute pure component values. Returns
        `a_alpha`, `da_alpha_dT`, and `d2a_alpha_dT2`. Calls 
        `setup_a_alpha_and_derivatives` before calling
        `a_alpha_and_derivatives` for each species, which typically sets `a` 
        and `Tc`. Calls `cleanup_a_alpha_and_derivatives` to remove the set
        properties after the calls are done.
        
        For use in `solve_T` this returns only `a_alpha` if `full` is False.
        
        .. math::
            a \alpha = \sum_i \sum_j z_i z_j {(a\alpha)}_{ij}
            
            (a\alpha)_{ij} = (1-k_{ij})\sqrt{(a\alpha)_{i}(a\alpha)_{j}}
        
        Parameters
        ----------
        T : float
            Temperature, [K]
        full : bool, optional
            If False, calculates and returns only `a_alpha`
        quick : bool, optional
            Only the quick variant is implemented; it is little faster anyhow
        
        Returns
        -------
        a_alpha : float
            Coefficient calculated by EOS-specific method, [J^2/mol^2/Pa]
        da_alpha_dT : float
            Temperature derivative of coefficient calculated by EOS-specific 
            method, [J^2/mol^2/Pa/K]
        d2a_alpha_dT2 : float
            Second temperature derivative of coefficient calculated by  
            EOS-specific method, [J^2/mol^2/Pa/K**2]

        Notes
        -----
        The exact expressions can be obtained with the following SymPy 
        expression below, commented out for brevity.
        
        >>> from sympy import *
        >>> a_alpha_i, a_alpha_j, kij, T = symbols('a_alpha_i, a_alpha_j, kij, T')
        >>> a_alpha_ij = (1-kij)*sqrt(a_alpha_i(T)*a_alpha_j(T))
        >>> #diff(a_alpha_ij, T)
        >>> #diff(a_alpha_ij, T, T)
        '''
        zs, kijs = self.zs, self.kijs
        a_alphas, da_alpha_dTs, d2a_alpha_dT2s = [], [], []
        
        for i in self.cmps:
            self.setup_a_alpha_and_derivatives(i, T=T)
            # Abuse method resolution order to call the a_alpha_and_derivatives
            # method of the original pure EOS
            # -4 goes back from object, GCEOS, SINGLEPHASEEOS, up to GCEOSMIX
            ds = super(type(self).__mro__[self.a_alpha_mro], self).a_alpha_and_derivatives(T)
            a_alphas.append(ds[0])
            da_alpha_dTs.append(ds[1])
            d2a_alpha_dT2s.append(ds[2])
        self.cleanup_a_alpha_and_derivatives()
        
        da_alpha_dT, d2a_alpha_dT2 = 0.0, 0.0
        
        a_alpha_ijs = [[(1. - kijs[i][j])*(a_alphas[i]*a_alphas[j])**0.5 
                              for j in self.cmps] for i in self.cmps]
                                
        # Needed in calculation of fugacity coefficients
        a_alpha = sum([a_alpha_ijs[i][j]*zs[i]*zs[j]
                      for j in self.cmps for i in self.cmps])
        self.a_alpha_ijs = a_alpha_ijs
        
        if full:
            for i in self.cmps:
                for j in self.cmps:
                    a_alphai, a_alphaj = a_alphas[i], a_alphas[j]
                    x0 = a_alphai*a_alphaj
                    x0_05 = x0**0.5
                    zi_zj = zs[i]*zs[j]

                    da_alpha_dT += zi_zj*((1. - kijs[i][j])/(2.*x0_05)
                    *(a_alphai*da_alpha_dTs[j] + a_alphaj*da_alpha_dTs[i]))
                    
                    x1 = a_alphai*da_alpha_dTs[j]
                    x2 = a_alphaj*da_alpha_dTs[i]
                    x3 = 2.*a_alphai*da_alpha_dTs[j] + 2.*a_alphaj*da_alpha_dTs[i]
                    d2a_alpha_dT2 += (-x0_05*(kijs[i][j] - 1.)*(x0*(
                    2.*a_alphai*d2a_alpha_dT2s[j] + 2.*a_alphaj*d2a_alpha_dT2s[i]
                    + 4.*da_alpha_dTs[i]*da_alpha_dTs[j]) - x1*x3 - x2*x3 + (x1 
                    + x2)**2)/(4.*x0*x0))*zi_zj
        
            return a_alpha, da_alpha_dT, d2a_alpha_dT2
        else:
            return a_alpha