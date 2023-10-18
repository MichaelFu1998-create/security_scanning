def SG(self):
        r'''Specific gravity of the mixture, [dimensionless]. 
        
        For gas-phase conditions, this is calculated at 15.6 °C (60 °F) and 1 
        atm for the mixture and the reference fluid, air. 
        For liquid and solid phase conditions, this is calculated based on a 
        reference fluid of water at 4°C at 1 atm, but the with the liquid or 
        solid mixture's density at the currently specified conditions.

        Examples
        --------
        >>> Mixture('MTBE').SG
        0.7428160596603596
        '''
        return phase_select_property(phase=self.phase, s=self.SGs, l=self.SGl, g=self.SGg)