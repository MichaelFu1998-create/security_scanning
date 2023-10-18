def rhol(self):
        r'''Liquid-phase mass density of the chemical at its current
        temperature and pressure, in units of [kg/m^3]. For calculation of this
        property at other temperatures and pressures, or specifying manually
        the method used to calculate it, and more - see the object oriented
        interface :obj:`thermo.volume.VolumeLiquid`; each Chemical instance
        creates one to actually perform the calculations. Note that that
        interface provides output in molar units.

        Examples
        --------
        >>> Chemical('o-xylene', T=297).rhol
        876.9946785618097
        '''
        Vml = self.Vml
        if Vml:
            return Vm_to_rho(Vml, self.MW)
        return None