def Pr(self):
        r'''Prandtl number of the chemical at its current temperature,
        pressure, and phase; [dimensionless].

        .. math::
            Pr = \frac{C_p \mu}{k}

        Examples
        --------
        >>> Chemical('acetone').Pr
        4.183039103542709
        '''
        return phase_select_property(phase=self.phase, l=self.Prl, g=self.Prg)