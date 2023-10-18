def Um(self):
        r'''Internal energy of the chemical at its current temperature and
        pressure, in units of [J/mol].

        This property requires that :obj:`thermo.chemical.set_thermo` ran
        successfully to be accurate.
        It also depends on the molar volume of the chemical at its current
        conditions.
        '''
        return self.Hm - self.P*self.Vm if (self.Vm and self.Hm is not None) else None