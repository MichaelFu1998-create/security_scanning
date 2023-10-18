def Parachor(self):
        r'''Parachor of the chemical at its
        current temperature and pressure, in units of [N^0.25*m^2.75/mol].

        .. math::
            P = \frac{\sigma^{0.25} MW}{\rho_L - \rho_V}

        Calculated based on surface tension, density of the liquid and gas
        phase, and molecular weight. For uses of this property, see
        :obj:`thermo.utils.Parachor`.

        Examples
        --------
        >>> Chemical('octane').Parachor
        6.291693072841486e-05
        '''
        sigma, rhol, rhog = self.sigma, self.rhol, self.rhog
        if all((sigma, rhol, rhog, self.MW)):
            return Parachor(sigma=sigma, MW=self.MW, rhol=rhol, rhog=rhog)
        return None