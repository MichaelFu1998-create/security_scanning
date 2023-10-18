def Am(self):
        r'''Helmholtz energy of the chemical at its current temperature and
        pressure, in units of [J/mol].

        This property requires that :obj:`thermo.chemical.set_thermo` ran
        successfully to be accurate.
        It also depends on the molar volume of the chemical at its current
        conditions.
        '''
        return self.Um - self.T*self.Sm if (self.Um is not None and self.Sm is not None) else None