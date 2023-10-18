def SGg(self):
        r'''Specific gravity of the gas phase of the chemical, [dimensionless].
        The reference condition is air at 15.6 °C (60 °F) and 1 atm 
        (rho=1.223 kg/m^3). The definition for gases uses the compressibility
        factor of the reference gas and the chemical both at the reference
        conditions, not the conditions of the chemical.
            
        Examples
        --------
        >>> Chemical('argon').SGg
        1.3795835970877504
        '''
        Vmg = self.VolumeGas(T=288.70555555555552, P=101325)
        if Vmg:
            rho = Vm_to_rho(Vmg, self.MW)
            return SG(rho, rho_ref=1.2231876628642968) # calculated with Mixture
        return None