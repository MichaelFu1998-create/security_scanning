def Hvap(self, T):
        r'''Method to calculate enthalpy of vaporization for a pure fluid from
        an equation of state, without iteration.
        
        .. math::
            \frac{dP^{sat}}{dT}=\frac{\Delta H_{vap}}{T(V_g - V_l)}
        
        Results above the critical temperature are meaningless. A first-order 
        polynomial is used to extrapolate under 0.32 Tc; however, there is 
        normally not a volume solution to the EOS which can produce that
        low of a pressure.
        
        Parameters
        ----------
        T : float
            Temperature, [K]

        Returns
        -------
        Hvap : float
            Increase in enthalpy needed for vaporization of liquid phase along 
            the saturation line, [J/mol]
            
        Notes
        -----
        Calculates vapor pressure and its derivative with `Psat` and `dPsat_dT`
        as well as molar volumes of the saturation liquid and vapor phase in
        the process.
        
        Very near the critical point this provides unrealistic results due to
        `Psat`'s polynomials being insufficiently accurate.
                    
        References
        ----------
        .. [1] Walas, Stanley M. Phase Equilibria in Chemical Engineering. 
           Butterworth-Heinemann, 1985.
        '''
        Psat = self.Psat(T)
        dPsat_dT = self.dPsat_dT(T)
        a_alpha = self.a_alpha_and_derivatives(T, full=False)
        Vs = self.volume_solutions(T, Psat, self.b, self.delta, self.epsilon, a_alpha)
        # Assume we can safely take the Vmax as gas, Vmin as l on the saturation line
        Vs = [i.real for i in Vs]
        V_l, V_g = min(Vs), max(Vs)
        return dPsat_dT*T*(V_g-V_l)