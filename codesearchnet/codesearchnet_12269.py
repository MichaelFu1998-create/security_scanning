def massradius(age, planetdist, coremass,
               mass='massjupiter',
               radius='radiusjupiter'):
    '''This function gets the Fortney mass-radius relation for planets.

    Parameters
    ----------

    age : float
        This should be one of: 0.3, 1.0, 4.5 [in Gyr].

    planetdist : float
        This should be one of: 0.02, 0.045, 0.1, 1.0, 9.5 [in AU]

    coremass : int
        This should be one of: 0, 10, 25, 50, 100 [in Mearth]

    mass : {'massjupiter','massearth'}
        Sets the mass units.

    radius : str
        Sets the radius units. Only 'radiusjupiter' is used for now.

    Returns
    -------

    dict
        A dict of the following form is returned::

            {'mass': an array containing the masses to plot),
             'radius': an array containing the radii to plot}

        These can be passed to a plotting routine to make mass-radius plot for
        the specified age, planet-star distance, and core-mass.

    '''

    MR = {0.3:MASSESRADII_0_3GYR,
          1.0:MASSESRADII_1_0GYR,
          4.5:MASSESRADII_4_5GYR}

    if age not in MR:
        print('given age not in Fortney 2007, returning...')
        return

    massradius = MR[age]

    if (planetdist in massradius) and (coremass in massradius[planetdist]):

        print('getting % Gyr M-R for planet dist %s AU, '
              'core mass %s Mearth...' % (age, planetdist, coremass))

        massradrelation = massradius[planetdist][coremass]

        outdict = {'mass':array(massradrelation[mass]),
                   'radius':array(massradrelation[radius])}

        return outdict