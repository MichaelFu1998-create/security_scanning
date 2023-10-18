def merge_hatpi_textlc_apertures(lclist):
    '''This merges all TFA text LCs with separate apertures for a single object.

    The framekey column will be used as the join column across all light curves
    in lclist. Missing values will be filled in with nans. This function assumes
    all light curves are in the format specified in COLDEFS above and readable
    by read_hatpi_textlc above (i.e. have a single column for TFA mags for a
    specific aperture at the end).

    '''

    lcaps = {}
    framekeys = []

    for lc in lclist:

        lcd = read_hatpi_textlc(lc)

        # figure what aperture this is and put it into the lcdict. if two LCs
        # with the same aperture (i.e. TF1 and TF1) are provided, the later one
        # in the lclist will overwrite the previous one,
        for col in lcd['columns']:
            if col.startswith('itf'):
                lcaps[col] = lcd
        thisframekeys = lcd['frk'].tolist()
        framekeys.extend(thisframekeys)

    # uniqify the framekeys
    framekeys = sorted(list(set(framekeys)))