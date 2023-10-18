def luminosity_within_ellipse_in_units(self, major_axis, unit_luminosity='eps', kpc_per_arcsec=None,
                                           exposure_time=None):
        """Integrate the light profiles to compute the total luminosity within an ellipse of specified major axis. \
        This is centred on the light profile's centre.

        The following units for mass can be specified and output:

        - Electrons per second (default) - 'eps'.
        - Counts - 'counts' (multiplies the luminosity in electrons per second by the exposure time).

        Parameters
        ----------
        major_axis : float
            The major-axis radius of the ellipse.
        unit_luminosity : str
            The units the luminosity is returned in (eps | counts).
        exposure_time : float or None
            The exposure time of the observation, which converts luminosity from electrons per second units to counts.
        """

        if not isinstance(major_axis, dim.Length):
            major_axis = dim.Length(major_axis, 'arcsec')

        profile = self.new_profile_with_units_converted(unit_length=major_axis.unit_length,
                                                        unit_luminosity=unit_luminosity,
                                                        kpc_per_arcsec=kpc_per_arcsec, exposure_time=exposure_time)
        luminosity = quad(profile.luminosity_integral, a=0.0, b=major_axis, args=(self.axis_ratio,))[0]
        return dim.Luminosity(luminosity, unit_luminosity)