def SGg(self):
        r'''Specific gravity of a hypothetical gas phase of the mixture, .
        [dimensionless]. The reference condition is air at 15.6 °C (60 °F) and 
        1 atm (rho=1.223 kg/m^3). The definition for gases uses the 
        compressibility factor of the reference gas and the mixture both at the 
        reference conditions, not the conditions of the mixture.
            
        Examples
        --------
        >>> Mixture('argon').SGg
        1.3800407778218216
        '''
        Vmg = self.VolumeGasMixture(T=288.70555555555552, P=101325, zs=self.zs, ws=self.ws)
        if Vmg:
            rho = Vm_to_rho(Vmg, self.MW)
            return SG(rho, rho_ref=1.2231876628642968) # calculated with Mixture
        return None