def API(self):
        r'''API gravity of the hypothetical liquid phase of the mixture, 
        [degrees]. The reference condition is water at 15.6 °C (60 °F) and 1 atm 
        (rho=999.016 kg/m^3, standardized).
            
        Examples
        --------
        >>> Mixture(['hexane', 'decane'], ws=[0.5, 0.5]).API
        71.34707841728181
        '''
        Vml = self.VolumeLiquidMixture(T=288.70555555555552, P=101325, zs=self.zs, ws=self.ws)
        if Vml:
            rho = Vm_to_rho(Vml, self.MW)
        sg = SG(rho, rho_ref=999.016)
        return SG_to_API(sg)