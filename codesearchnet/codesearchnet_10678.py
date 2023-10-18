def luminosity_within_circle_in_units(self, radius: dim.Length, unit_luminosity='eps', kpc_per_arcsec=None,
                                          exposure_time=None):
        """Integrate the light profile to compute the total luminosity within a circle of specified radius. This is \
        centred on the light profile's centre.

        The following units for mass can be specified and output:

        - Electrons per second (default) - 'eps'.
        - Counts - 'counts' (multiplies the luminosity in electrons per second by the exposure time).

        Parameters
        ----------
        radius : float
            The radius of the circle to compute the dimensionless mass within.
        unit_luminosity : str
            The units the luminosity is returned in (eps | counts).
        exposure_time : float or None
            The exposure time of the observation, which converts luminosity from electrons per second units to counts.
        """

        if not isinstance(radius, dim.Length):
            radius = dim.Length(value=radius, unit_length='arcsec')

        profile = self.new_profile_with_units_converted(unit_length=radius.unit_length, unit_luminosity=unit_luminosity,
                                                        kpc_per_arcsec=kpc_per_arcsec, exposure_time=exposure_time)

        luminosity = quad(profile.luminosity_integral, a=0.0, b=radius, args=(1.0,))[0]
        return dim.Luminosity(luminosity, unit_luminosity)