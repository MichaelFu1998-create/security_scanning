def normalized_flux_to_mag(lcdict,
                           columns=('sap.sap_flux',
                                    'sap.sap_flux_err',
                                    'sap.sap_bkg',
                                    'sap.sap_bkg_err',
                                    'pdc.pdcsap_flux',
                                    'pdc.pdcsap_flux_err')):
    '''This converts the normalized fluxes in the TESS lcdicts to TESS mags.

    Uses the object's TESS mag stored in lcdict['objectinfo']['tessmag']::

        mag - object_tess_mag = -2.5 log (flux/median_flux)

    Parameters
    ----------

    lcdict : lcdict
        An `lcdict` produced by `read_tess_fitslc` or
        `consolidate_tess_fitslc`. This must have normalized fluxes in its
        measurement columns (use the `normalize` kwarg for these functions).

    columns : sequence of str
        The column keys of the normalized flux and background measurements in
        the `lcdict` to operate on and convert to magnitudes in TESS band (T).

    Returns
    -------

    lcdict
        The returned `lcdict` will contain extra columns corresponding to
        magnitudes for each input normalized flux/background column.

    '''

    tess_mag = lcdict['objectinfo']['tessmag']

    for key in columns:

        k1, k2 = key.split('.')

        if 'err' not in k2:

            lcdict[k1][k2.replace('flux','mag')] = (
                tess_mag - 2.5*np.log10(lcdict[k1][k2])
            )

        else:

            lcdict[k1][k2.replace('flux','mag')] = (
                - 2.5*np.log10(1.0 - lcdict[k1][k2])
            )

    return lcdict