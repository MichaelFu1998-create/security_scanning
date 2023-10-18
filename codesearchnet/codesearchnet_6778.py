def solve_T(self, P, V, quick=True):
        r'''Method to calculate `T` from a specified `P` and `V` for the RK
        EOS. Uses `a`, and `b`, obtained from the class's namespace.

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
        The exact solution can be derived as follows; it is excluded for 
        breviety.
        
        >>> from sympy import *
        >>> P, T, V, R = symbols('P, T, V, R')
        >>> Tc, Pc = symbols('Tc, Pc')
        >>> a, b = symbols('a, b')

        >>> RK = Eq(P, R*T/(V-b) - a/sqrt(T)/(V*V + b*V))
        >>> # solve(RK, T)
        '''
        a, b = self.a, self.b
        if quick:
            x1 = -1.j*1.7320508075688772 + 1.
            x2 = V - b
            x3 = x2/R
            x4 = V + b
            x5 = (1.7320508075688772*(x2*x2*(-4.*P*P*P*x3 + 27.*a*a/(V*V*x4*x4))/(R*R))**0.5 - 9.*a*x3/(V*x4) +0j)**(1./3.)
            return (3.3019272488946263*(11.537996562459266*P*x3/(x1*x5) + 1.2599210498948732*x1*x5)**2/144.0).real
        else:
            return ((-(-1/2 + sqrt(3)*1j/2)*(sqrt(729*(-V*a + a*b)**2/(R*V**2 + R*V*b)**2 + 108*(-P*V + P*b)**3/R**3)/2 + 27*(-V*a + a*b)/(2*(R*V**2 + R*V*b))+0j)**(1/3)/3 + (-P*V + P*b)/(R*(-1/2 + sqrt(3)*1j/2)*(sqrt(729*(-V*a + a*b)**2/(R*V**2 + R*V*b)**2 + 108*(-P*V + P*b)**3/R**3)/2 + 27*(-V*a + a*b)/(2*(R*V**2 + R*V*b))+0j)**(1/3)))**2).real