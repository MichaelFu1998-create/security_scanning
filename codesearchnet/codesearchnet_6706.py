def API(self):
        r'''API gravity of the liquid phase of the chemical, [degrees].
        The reference condition is water at 15.6 °C (60 °F) and 1 atm 
        (rho=999.016 kg/m^3, standardized).
            
        Examples
        --------
        >>> Chemical('water').API
        9.999752435378895
        '''
        Vml = self.VolumeLiquid(T=288.70555555555552, P=101325)
        if Vml:
            rho = Vm_to_rho(Vml, self.MW)
        sg = SG(rho, rho_ref=999.016)
        return SG_to_API(sg)