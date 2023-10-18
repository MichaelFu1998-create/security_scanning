def SG(self):
        r'''Specific gravity of the chemical, [dimensionless]. 
        
        For gas-phase conditions, this is calculated at 15.6 °C (60 °F) and 1 
        atm for the chemical and the reference fluid, air. 
        For liquid and solid phase conditions, this is calculated based on a 
        reference fluid of water at 4°C at 1 atm, but the with the liquid or 
        solid chemical's density at the currently specified conditions.

        Examples
        --------
        >>> Chemical('MTBE').SG
        0.7428160596603596
        '''
        phase = self.phase
        if phase == 'l':
            return self.SGl
        elif phase == 's':
            return self.SGs
        elif phase == 'g':
            return self.SGg
        rho = self.rho
        if rho is not None:
            return SG(rho)
        return None