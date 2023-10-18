def A(self):
        r'''Helmholtz energy of the chemical at its current temperature and
        pressure, in units of [J/kg].

        This property requires that :obj:`thermo.chemical.set_thermo` ran
        successfully to be accurate.
        It also depends on the molar volume of the chemical at its current
        conditions.
        '''
        return self.U - self.T*self.S if (self.U is not None and self.S is not None) else None