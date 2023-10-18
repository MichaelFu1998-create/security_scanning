def _process_flux_dataframe(flux_dataframe, fva, threshold, floatfmt):
    """Some common methods for processing a database of flux information into
    print-ready formats. Used in both model_summary and metabolite_summary. """

    abs_flux = flux_dataframe['flux'].abs()
    flux_threshold = threshold * abs_flux.max()

    # Drop unused boundary fluxes
    if fva is None:
        flux_dataframe = flux_dataframe.loc[
            abs_flux >= flux_threshold, :].copy()
    else:
        flux_dataframe = flux_dataframe.loc[
            (abs_flux >= flux_threshold) |
            (flux_dataframe['fmin'].abs() >= flux_threshold) |
            (flux_dataframe['fmax'].abs() >= flux_threshold), :].copy()

        # Why set to zero? If included show true value?
        # flux_dataframe.loc[
        #     flux_dataframe['flux'].abs() < flux_threshold, 'flux'] = 0

    # Make all fluxes positive
    if fva is None:
        flux_dataframe['is_input'] = (flux_dataframe['flux'] >= 0)
        flux_dataframe['flux'] = flux_dataframe['flux'].abs()
    else:

        def get_direction(flux, fmin, fmax):
            """ decide whether or not to reverse a flux to make it positive """

            if flux < 0:
                return -1
            elif flux > 0:
                return 1
            elif (fmax > 0) & (fmin <= 0):
                return 1
            elif (fmax < 0) & (fmin >= 0):
                return -1
            elif ((fmax + fmin) / 2) < 0:
                return -1
            else:
                return 1

        sign = flux_dataframe.apply(
            lambda x: get_direction(x.flux, x.fmin, x.fmax), 1)

        flux_dataframe['is_input'] = sign == 1

        flux_dataframe.loc[:, ['flux', 'fmin', 'fmax']] = \
            flux_dataframe.loc[:, ['flux', 'fmin', 'fmax']].multiply(
                sign, 0).astype('float').round(6)

        flux_dataframe.loc[:, ['flux', 'fmin', 'fmax']] = \
            flux_dataframe.loc[:, ['flux', 'fmin', 'fmax']].applymap(
                lambda x: x if abs(x) > 1E-6 else 0)

    if fva is not None:
        flux_dataframe['fva_fmt'] = flux_dataframe.apply(
            lambda x: ("[{0.fmin:" + floatfmt + "}, {0.fmax:" +
                       floatfmt + "}]").format(x), 1)

        flux_dataframe = flux_dataframe.sort_values(
            by=['flux', 'fmax', 'fmin', 'id'],
            ascending=[False, False, False, True])

    else:
        flux_dataframe = flux_dataframe.sort_values(
            by=['flux', 'id'], ascending=[False, True])

    return flux_dataframe