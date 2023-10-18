def rhog(self):
        r'''Gas-phase mass density of the chemical at its current temperature
        and pressure, in units of [kg/m^3]. For calculation of this property at
        other temperatures or pressures, or specifying manually the method used
        to calculate it, and more - see the object oriented interface
        :obj:`thermo.volume.VolumeGas`; each Chemical instance
        creates one to actually perform the calculations. Note that that
        interface provides output in molar units.

        Examples
        --------
        Estimate the density of the core of the sun, at 15 million K and
        26.5 PetaPascals, assuming pure helium (actually 68% helium):

        >>> Chemical('helium', T=15E6, P=26.5E15).rhog
        8329.27226509739

        Compared to a result on
        `Wikipedia <https://en.wikipedia.org/wiki/Solar_core>`_ of 150000
        kg/m^3, the fundamental equation of state performs poorly.

        >>> He = Chemical('helium', T=15E6, P=26.5E15)
        >>> He.VolumeGas.set_user_methods_P(['IDEAL']); He.rhog
        850477.8065477367

        The ideal-gas law performs somewhat better, but vastly overshoots
        the density prediction.
        '''
        Vmg = self.Vmg
        if Vmg:
            return Vm_to_rho(Vmg, self.MW)
        return None