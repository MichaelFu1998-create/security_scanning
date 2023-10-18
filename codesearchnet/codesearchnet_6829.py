def entropy_Cpg_Hvap(self):
        r'''Method to calculate the entropy of an ideal mixture. This routine 
        is based on "route A", where only the gas heat capacity and enthalpy of
        vaporization are used.
        
        The reference temperature and pressure are properties of the class; it 
        defaults to 298.15 K and 101325 Pa.
        
        There is a contribution due to mixing:
            
        .. math::
            \Delta S_{mixing} = -R\sum_i z_i \log(z_i) 
            
        The ideal gas pressure contribution is:
            
        .. math::
            \Delta S_{P} = -R\log\left(\frac{P}{P_{ref}}\right)
            
        For a liquid mixture or a partially liquid mixture, the entropy
        contribution is not so strong - all such pressure effects find that
        expression capped at the vapor pressure, as shown in [1]_.
        
        .. math::
            \Delta S_{P} = - \sum_i x_i\left(1 - \frac{V}{F}\right) 
            R\log\left(\frac{P_{sat, i}}{P_{ref}}\right) - \sum_i y_i\left(
            \frac{V}{F}\right) R\log\left(\frac{P}{P_{ref}}\right)
            
        These expressions are combined with the standard heat capacity and 
        enthalpy of vaporization expressions to calculate the total entropy:
        
        For a pure gas mixture:
            
        .. math::
             S = \Delta S_{mixing} + \Delta S_{P} + \sum_i z_i \cdot
             \int_{T_{ref}}^T \frac{C_{p}^{ig}(T)}{T} dT
                          
        For a pure liquid mixture:
            
        .. math::
             S = \Delta S_{mixing} + \Delta S_{P} + \sum_i z_i \left( 
             \int_{T_{ref}}^T \frac{C_{p}^{ig}(T)}{T} dT + \frac{H_{vap, i}
             (T)}{T} \right)
            
        For a vapor-liquid mixture:
            
        .. math::
             S = \Delta S_{mixing} + \Delta S_{P} + \sum_i z_i \cdot 
             \int_{T_{ref}}^T \frac{C_{p}^{ig}(T)}{T} dT + \sum_i x_i\left(1
             - \frac{V}{F}\right)\frac{H_{vap, i}(T)}{T}
             
        Returns
        -------
        S : float
            Entropy of the mixture with respect to the reference temperature,
            [J/mol/K]
            
        Notes
        -----
        The object must be flashed before this routine can be used. It 
        depends on the properties T, P, zs, V_over_F, HeatCapacityGases, 
        EnthalpyVaporizations, VaporPressures, and xs.
        
        References
        ----------
        .. [1] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
           New York: McGraw-Hill Professional, 2000.
        '''
        S = 0
        T = self.T
        P = self.P
        S -= R*sum([zi*log(zi) for zi in self.zs if zi > 0]) # ideal composition entropy composition; chemsep checked
        # Both of the mixing and vapor pressure terms have negative signs
        # Equation 6-4.4b in Poling for the vapor pressure component
        # For liquids above their critical temperatures, Psat is equal to the system P (COCO).
        if self.phase == 'g':
            S -= R*log(P/101325.) # Gas-phase ideal pressure contribution (checked repeatedly)
            for i in self.cmps:
                S += self.HeatCapacityGases[i].T_dependent_property_integral_over_T(298.15, T)
        elif self.phase == 'l':
            Psats = self._Psats(T)
            for i in self.cmps:
                Sg298_to_T = self.HeatCapacityGases[i].T_dependent_property_integral_over_T(298.15, T)
                Hvap = self.EnthalpyVaporizations[i](T)
                if Hvap is None:
                    Hvap = 0 # Handle the case of a package predicting a transition past the Tc
                Svap = -Hvap/T # Do the transition at the temperature of the liquid
                S_P = -R*log(Psats[i]/101325.)
                S += self.zs[i]*(Sg298_to_T + Svap + S_P)
        elif self.phase == 'l/g':
            Psats = self._Psats(T)
            S_P_vapor = -R*log(P/101325.) # Gas-phase ideal pressure contribution (checked repeatedly)
            for i in self.cmps:
                Sg298_to_T_zi = self.zs[i]*self.HeatCapacityGases[i].T_dependent_property_integral_over_T(298.15, T)
                Hvap = self.EnthalpyVaporizations[i](T) 
                if Hvap is None:
                    Hvap = 0 # Handle the case of a package predicting a transition past the Tc

                Svap_contrib = -self.xs[i]*(1-self.V_over_F)*Hvap/T
                # Pressure contributions from both phases
                S_P_vapor_i = self.V_over_F*self.ys[i]*S_P_vapor
                S_P_liquid_i = -R*log(Psats[i]/101325.)*(1-self.V_over_F)*self.xs[i]
                S += (Sg298_to_T_zi + Svap_contrib + S_P_vapor_i + S_P_liquid_i)
        return S