def Poynting(self):
        r'''Poynting correction factor [dimensionless] for use in phase 
        equilibria methods based on activity coefficients or other reference 
        states. Performs the shortcut calculation assuming molar volume is 
        independent of pressure.

        .. math::
            \text{Poy} =  \exp\left[\frac{V_l (P-P^{sat})}{RT}\right]

        The full calculation normally returns values very close to the
        approximate ones. This property is defined in terms of
        pure components only.

        Examples
        --------
        >>> Chemical('pentane', T=300, P=1E7).Poynting
        1.5743051250679803

        Notes
        -----
        The full equation shown below can be used as follows:

        .. math::
            \text{Poy} = \exp\left[\frac{\int_{P_i^{sat}}^P V_i^l dP}{RT}\right]

        >>> from scipy.integrate import quad
        >>> c = Chemical('pentane', T=300, P=1E7)
        >>> exp(quad(lambda P : c.VolumeLiquid(c.T, P), c.Psat, c.P)[0]/R/c.T)
        1.5821826990975127
        '''
        Vml, Psat = self.Vml, self.Psat
        if Vml and Psat:
            return exp(Vml*(self.P-Psat)/R/self.T)
        return None