def concatenate_textlcs(lclist,
                        sortby='rjd',
                        normalize=True):
    '''This concatenates a list of light curves.

    Does not care about overlaps or duplicates. The light curves must all be
    from the same aperture.

    The intended use is to concatenate light curves across CCDs or instrument
    changes for a single object. These can then be normalized later using
    standard astrobase tools to search for variablity and/or periodicity.

    sortby is a column to sort the final concatenated light curve by in
    ascending order.

    If normalize is True, then each light curve's magnitude columns are
    normalized to zero.

    The returned lcdict has an extra column: 'lcn' that tracks which measurement
    belongs to which input light curve. This can be used with
    lcdict['concatenated'] which relates input light curve index to input light
    curve filepath. Finally, there is an 'nconcatenated' key in the lcdict that
    contains the total number of concatenated light curves.

    '''

    # read the first light curve
    lcdict = read_hatpi_textlc(lclist[0])

    # track which LC goes where
    # initial LC
    lccounter = 0
    lcdict['concatenated'] = {lccounter: os.path.abspath(lclist[0])}
    lcdict['lcn'] = np.full_like(lcdict['rjd'], lccounter)

    # normalize if needed
    if normalize:

        for col in MAGCOLS:

            if col in lcdict:
                thismedval = np.nanmedian(lcdict[col])

                # handle fluxes
                if col in ('ifl1','ifl2','ifl3'):
                    lcdict[col] = lcdict[col] / thismedval
                # handle mags
                else:
                    lcdict[col] = lcdict[col] - thismedval

    # now read the rest
    for lcf in lclist[1:]:

        thislcd = read_hatpi_textlc(lcf)

        # if the columns don't agree, skip this LC
        if thislcd['columns'] != lcdict['columns']:
            LOGERROR('file %s does not have the '
                     'same columns as first file %s, skipping...'
                     % (lcf, lclist[0]))
            continue

        # otherwise, go ahead and start concatenatin'
        else:

            LOGINFO('adding %s (ndet: %s) to %s (ndet: %s)'
                    % (lcf,
                       thislcd['objectinfo']['ndet'],
                       lclist[0],
                       lcdict[lcdict['columns'][0]].size))

            # update LC tracking
            lccounter = lccounter + 1
            lcdict['concatenated'][lccounter] = os.path.abspath(lcf)
            lcdict['lcn'] = np.concatenate((
                lcdict['lcn'],
                np.full_like(thislcd['rjd'],lccounter)
            ))

            # concatenate the columns
            for col in lcdict['columns']:

                # handle normalization for magnitude columns
                if normalize and col in MAGCOLS:

                    thismedval = np.nanmedian(thislcd[col])

                    # handle fluxes
                    if col in ('ifl1','ifl2','ifl3'):
                        thislcd[col] = thislcd[col] / thismedval
                    # handle mags
                    else:
                        thislcd[col] = thislcd[col] - thismedval

                # concatenate the values
                lcdict[col] = np.concatenate((lcdict[col], thislcd[col]))

    #
    # now we're all done concatenatin'
    #

    # make sure to add up the ndet
    lcdict['objectinfo']['ndet'] = lcdict[lcdict['columns'][0]].size

    # update the stations
    lcdict['objectinfo']['stations'] = [
        'HP%s' % x for x in np.unique(lcdict['stf']).tolist()
    ]

    # update the total LC count
    lcdict['nconcatenated'] = lccounter + 1

    # if we're supposed to sort by a column, do so
    if sortby and sortby in [x[0] for x in COLDEFS]:

        LOGINFO('sorting concatenated light curve by %s...' % sortby)
        sortind = np.argsort(lcdict[sortby])

        # sort all the measurement columns by this index
        for col in lcdict['columns']:
            lcdict[col] = lcdict[col][sortind]

        # make sure to sort the lcn index as well
        lcdict['lcn'] = lcdict['lcn'][sortind]

    LOGINFO('done. concatenated light curve has %s detections' %
            lcdict['objectinfo']['ndet'])
    return lcdict