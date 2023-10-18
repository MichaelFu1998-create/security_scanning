def solve_T(self, P, V):
        r'''Method to calculate `T` from a specified `P` and `V` for the VDW
        EOS. Uses `a`, and `b`, obtained from the class's namespace.

        .. math::
            T =  \frac{1}{R V^{2}} \left(P V^{2} \left(V - b\right)
            + V a - a b\right)

        Parameters
        ----------
        P : float
            Pressure, [Pa]
        V : float
            Molar volume, [m^3/mol]

        Returns
        -------
        T : float
            Temperature, [K]
        '''
        return (P*V**2*(V - self.b) + V*self.a - self.a*self.b)/(R*V**2)