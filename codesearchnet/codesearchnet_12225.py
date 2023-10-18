def read_hatpi_binnedlc(binnedpklf, textlcf, timebinsec):
    '''This reads a binnedlc pickle produced by the HATPI prototype pipeline.

    Converts it into a standard lcdict as produced by the read_hatpi_textlc
    function above by using the information in unbinnedtextlc for the same
    object.

    Adds a 'binned' key to the standard lcdict containing the binned mags, etc.

    '''

    LOGINFO('reading binned LC %s' % binnedpklf)

    # read the textlc
    lcdict = read_hatpi_textlc(textlcf)

    # read the binned LC

    if binnedpklf.endswith('.gz'):
        infd = gzip.open(binnedpklf,'rb')
    else:
        infd = open(binnedpklf,'rb')


    try:
        binned = pickle.load(infd)
    except Exception as e:
        infd.seek(0)
        binned = pickle.load(infd, encoding='latin1')
    infd.close()

    # now that we have both, pull out the required columns from the binnedlc
    blckeys = binned.keys()

    lcdict['binned'] = {}

    for key in blckeys:

        # get EPD stuff
        if (key == 'epdlc' and
            'AP0' in binned[key] and
            'AP1' in binned[key] and
            'AP2' in binned[key]):

            # we'll have to generate errors because we don't have any in the
            # generated binned LC.

            ap0mad = np.nanmedian(np.abs(binned[key]['AP0'] -
                                         np.nanmedian(binned[key]['AP0'])))
            ap1mad = np.nanmedian(np.abs(binned[key]['AP1'] -
                                         np.nanmedian(binned[key]['AP1'])))
            ap2mad = np.nanmedian(np.abs(binned[key]['AP2'] -
                                         np.nanmedian(binned[key]['AP2'])))


            lcdict['binned']['iep1'] = {'times':binned[key]['RJD'],
                                        'mags':binned[key]['AP0'],
                                        'errs':np.full_like(binned[key]['AP0'],
                                                            ap0mad),
                                        'nbins':binned[key]['nbins'],
                                        'timebins':binned[key]['jdbins'],
                                        'timebinsec':timebinsec}
            lcdict['binned']['iep2'] = {'times':binned[key]['RJD'],
                                        'mags':binned[key]['AP1'],
                                        'errs':np.full_like(binned[key]['AP1'],
                                                            ap1mad),
                                        'nbins':binned[key]['nbins'],
                                        'timebins':binned[key]['jdbins'],
                                        'timebinsec':timebinsec}
            lcdict['binned']['iep3'] = {'times':binned[key]['RJD'],
                                        'mags':binned[key]['AP2'],
                                        'errs':np.full_like(binned[key]['AP2'],
                                                            ap2mad),
                                        'nbins':binned[key]['nbins'],
                                        'timebins':binned[key]['jdbins'],
                                        'timebinsec':timebinsec}

        # get TFA stuff for aperture 1
        if ((key == 'tfalc.TF1' or key == 'tfalc.TF1.gz') and
            'AP0' in binned[key]):

            # we'll have to generate errors because we don't have any in the
            # generated binned LC.

            ap0mad = np.nanmedian(np.abs(binned[key]['AP0'] -
                                         np.nanmedian(binned[key]['AP0'])))


            lcdict['binned']['itf1'] = {'times':binned[key]['RJD'],
                                        'mags':binned[key]['AP0'],
                                        'errs':np.full_like(binned[key]['AP0'],
                                                            ap0mad),
                                        'nbins':binned[key]['nbins'],
                                        'timebins':binned[key]['jdbins'],
                                        'timebinsec':timebinsec}

        # get TFA stuff for aperture 1
        if ((key == 'tfalc.TF2' or key == 'tfalc.TF2.gz') and
            'AP0' in binned[key]):

            # we'll have to generate errors because we don't have any in the
            # generated binned LC.

            ap0mad = np.nanmedian(np.abs(binned[key]['AP0'] -
                                         np.nanmedian(binned[key]['AP0'])))


            lcdict['binned']['itf2'] = {'times':binned[key]['RJD'],
                                        'mags':binned[key]['AP0'],
                                        'errs':np.full_like(binned[key]['AP0'],
                                                            ap0mad),
                                        'nbins':binned[key]['nbins'],
                                        'timebins':binned[key]['jdbins'],
                                        'timebinsec':timebinsec}

        # get TFA stuff for aperture 1
        if ((key == 'tfalc.TF3' or key == 'tfalc.TF3.gz') and
            'AP0' in binned[key]):

            # we'll have to generate errors because we don't have any in the
            # generated binned LC.

            ap0mad = np.nanmedian(np.abs(binned[key]['AP0'] -
                                         np.nanmedian(binned[key]['AP0'])))


            lcdict['binned']['itf3'] = {'times':binned[key]['RJD'],
                                        'mags':binned[key]['AP0'],
                                        'errs':np.full_like(binned[key]['AP0'],
                                                            ap0mad),
                                        'nbins':binned[key]['nbins'],
                                        'timebins':binned[key]['jdbins'],
                                        'timebinsec':timebinsec}

    # all done, check if we succeeded
    if lcdict['binned']:

        return lcdict

    else:

        LOGERROR('no binned measurements found in %s!' % binnedpklf)
        return None