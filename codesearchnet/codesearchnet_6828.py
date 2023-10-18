def enthalpy_Cpg_Hvap(self):
        r'''Method to calculate the enthalpy of an ideal mixture (no pressure
        effects). This routine is based on "route A", where only the gas heat
        capacity and enthalpy of vaporization are used.
        
        The reference temperature is a property of the class; it defaults to
        298.15 K.
        
        For a pure gas mixture:
            
        .. math::
             H = \sum_i z_i \cdot \int_{T_{ref}}^T C_{p}^{ig}(T) dT
             
        For a pure liquid mixture:
            
        .. math::
             H = \sum_i z_i \left( \int_{T_{ref}}^T C_{p}^{ig}(T) dT + H_{vap, i}(T) \right)
             
        For a vapor-liquid mixture:
            
        .. math::
             H = \sum_i z_i \cdot \int_{T_{ref}}^T C_{p}^{ig}(T) dT
                 + \sum_i x_i\left(1 - \frac{V}{F}\right)H_{vap, i}(T)

        Returns
        -------
        H : float
            Enthalpy of the mixture with respect to the reference temperature,
            [J/mol]
            
        Notes
        -----
        The object must be flashed before this routine can be used. It 
        depends on the properties T, zs, xs, V_over_F, HeatCapacityGases, 
        EnthalpyVaporizations, and.
        '''
        H = 0
        T = self.T
        if self.phase == 'g':
            for i in self.cmps:
                H += self.zs[i]*self.HeatCapacityGases[i].T_dependent_property_integral(self.T_REF_IG, T)
        elif self.phase == 'l':
            for i in self.cmps:
                # No further contribution needed
                Hg298_to_T = self.HeatCapacityGases[i].T_dependent_property_integral(self.T_REF_IG, T)
                Hvap = self.EnthalpyVaporizations[i](T) # Do the transition at the temperature of the liquid
                if Hvap is None:
                    Hvap = 0 # Handle the case of a package predicting a transition past the Tc
                H += self.zs[i]*(Hg298_to_T - Hvap)
        elif self.phase == 'l/g':
            for i in self.cmps:
                Hg298_to_T_zi = self.zs[i]*self.HeatCapacityGases[i].T_dependent_property_integral(self.T_REF_IG, T)
                Hvap = self.EnthalpyVaporizations[i](T) 
                if Hvap is None:
                    Hvap = 0 # Handle the case of a package predicting a transition past the Tc
                Hvap_contrib = -self.xs[i]*(1-self.V_over_F)*Hvap
                H += (Hg298_to_T_zi + Hvap_contrib)
        return H