def rhom(self):
        r'''Molar density of the mixture at its current phase and
        temperature and pressure, in units of [mol/m^3].
        Available only if single phase.

        Examples
        --------
        >>> Mixture(['1-hexanol'], ws=[1]).rhom
        7983.414573003429
        '''
        return phase_select_property(phase=self.phase, s=None, l=self.rholm, g=self.rhogm)