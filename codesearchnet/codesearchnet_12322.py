def _make_periodogram(axes,
                      lspinfo,
                      objectinfo,
                      findercmap,
                      finderconvolve,
                      verbose=True,
                      findercachedir='~/.astrobase/stamp-cache'):
    '''Makes periodogram, objectinfo, and finder tile for `checkplot_png` and
    `twolsp_checkplot_png`.

    Parameters
    ----------

    axes : matplotlib.axes.Axes object
        The Axes object which will contain the plot being made.

    lspinfo : dict
        Dict containing results from a period-finder in `astrobase.periodbase`
        or a dict that corresponds to that format.

    objectinfo : dict
        Dict containing basic info about the object being processed.

    findercmap : matplotlib Colormap object or str
        The Colormap object to use for the finder chart image.

    finderconvolve : astropy.convolution.Kernel object or None
        If not None, the Kernel object to use for convolving the finder image.

    verbose : bool
        If True, indicates progress.

    findercachedir : str
        The directory where the FITS finder images are downloaded and cached.

    Returns
    -------

    Does not return anything, works on the input Axes object directly.

    '''

    # get the appropriate plot ylabel
    pgramylabel = PLOTYLABELS[lspinfo['method']]

    # get the periods and lspvals from lspinfo
    periods = lspinfo['periods']
    lspvals = lspinfo['lspvals']
    bestperiod = lspinfo['bestperiod']
    nbestperiods = lspinfo['nbestperiods']
    nbestlspvals = lspinfo['nbestlspvals']

    # make the LSP plot on the first subplot
    axes.plot(periods,lspvals)

    axes.set_xscale('log',basex=10)
    axes.set_xlabel('Period [days]')
    axes.set_ylabel(pgramylabel)
    plottitle = '%s - %.6f d' % (METHODLABELS[lspinfo['method']],
                                 bestperiod)
    axes.set_title(plottitle)

    # show the best five peaks on the plot
    for bestperiod, bestpeak in zip(nbestperiods,
                                    nbestlspvals):
        axes.annotate('%.6f' % bestperiod,
                      xy=(bestperiod, bestpeak), xycoords='data',
                      xytext=(0.0,25.0), textcoords='offset points',
                      arrowprops=dict(arrowstyle="->"),fontsize='14.0')

    # make a grid
    axes.grid(color='#a9a9a9',
              alpha=0.9,
              zorder=0,
              linewidth=1.0,
              linestyle=':')


    # if objectinfo is present, get things from it
    if (objectinfo and isinstance(objectinfo, dict) and
        ('objectid' in objectinfo or 'hatid' in objectinfo) and
        'ra' in objectinfo and 'decl' in objectinfo and
        objectinfo['ra'] and objectinfo['decl']):

        if 'objectid' not in objectinfo:
            objectid = objectinfo['hatid']
        else:
            objectid = objectinfo['objectid']

        if verbose:
            LOGINFO('adding in object information and '
                    'finder chart for %s at RA: %.3f, DEC: %.3f' %
                    (objectid, objectinfo['ra'], objectinfo['decl']))


        # calculate colors
        if ('bmag' in objectinfo and 'vmag' in objectinfo and
            'jmag' in objectinfo and 'kmag' in objectinfo and
            'sdssi' in objectinfo and
            objectinfo['bmag'] and objectinfo['vmag'] and
            objectinfo['jmag'] and objectinfo['kmag'] and
            objectinfo['sdssi']):
            bvcolor = objectinfo['bmag'] - objectinfo['vmag']
            jkcolor = objectinfo['jmag'] - objectinfo['kmag']
            ijcolor = objectinfo['sdssi'] - objectinfo['jmag']
        else:
            bvcolor = None
            jkcolor = None
            ijcolor = None

        if ('teff' in objectinfo and 'gmag' in objectinfo and
            objectinfo['teff'] and objectinfo['gmag']):
            # Gaia data input
            teff_val = objectinfo['teff']
            gmag = objectinfo['gmag']


        # bump the ylim of the LSP plot so that the overplotted finder and
        # objectinfo can fit in this axes plot
        lspylim = axes.get_ylim()
        axes.set_ylim(lspylim[0], lspylim[1]+0.75*(lspylim[1]-lspylim[0]))

        # get the stamp
        try:
            dss, dssheader = skyview_stamp(objectinfo['ra'],
                                           objectinfo['decl'],
                                           convolvewith=finderconvolve,
                                           flip=False,
                                           cachedir=findercachedir,
                                           verbose=verbose)
            stamp = dss

            # inset plot it on the current axes
            inset = inset_axes(axes, width="40%", height="40%", loc=1)
            inset.imshow(stamp, cmap=findercmap, origin='lower')
            inset.set_xticks([])
            inset.set_yticks([])
            inset.set_frame_on(False)

            # grid lines pointing to the center of the frame
            inset.axvline(x=150,ymin=0.375,ymax=0.45,linewidth=2.0,color='b')
            inset.axhline(y=150,xmin=0.375,xmax=0.45,linewidth=2.0,color='b')

        except OSError as e:

            LOGERROR('downloaded FITS appears to be corrupt, retrying...')

            dss, dssheader = skyview_stamp(objectinfo['ra'],
                                           objectinfo['decl'],
                                           convolvewith=finderconvolve,
                                           flip=False,
                                           forcefetch=True,
                                           cachedir=findercachedir,
                                           verbose=verbose)
            stamp = dss

            # inset plot it on the current axes
            inset = inset_axes(axes, width="40%", height="40%", loc=1)
            inset.imshow(stamp, cmap=findercmap, origin='lower')
            inset.set_xticks([])
            inset.set_yticks([])
            inset.set_frame_on(False)

            # grid lines pointing to the center of the frame
            inset.axvline(x=150,ymin=0.375,ymax=0.45,linewidth=2.0,color='b')
            inset.axhline(y=150,xmin=0.375,xmax=0.45,linewidth=2.0,color='b')


        except Exception as e:
            LOGEXCEPTION('could not fetch a DSS stamp for this '
                         'object %s using coords (%.3f,%.3f)' %
                         (objectid, objectinfo['ra'], objectinfo['decl']))

        # annotate with objectinfo
        axes.text(
            0.05,0.95,
            '%s' % objectid,
            ha='left',va='center',transform=axes.transAxes,
            fontsize=18.0
        )

        axes.text(
            0.05,0.91,
            'RA = %.3f, DEC = %.3f' % (objectinfo['ra'], objectinfo['decl']),
            ha='left',va='center',transform=axes.transAxes,
            fontsize=18.0
        )

        if bvcolor:
            axes.text(0.05,0.87,
                      '$B - V$ = %.3f, $V$ = %.3f' % (bvcolor,
                                                      objectinfo['vmag']),
                      ha='left',va='center',transform=axes.transAxes,
                      fontsize=18.0)
        elif 'vmag' in objectinfo and objectinfo['vmag']:
            axes.text(0.05,0.87,
                      '$V$ = %.3f' % (objectinfo['vmag'],),
                      ha='left',va='center',transform=axes.transAxes,
                      fontsize=18.0)

        if ijcolor:
            axes.text(0.05,0.83,
                      '$i - J$ = %.3f, $J$ = %.3f' % (ijcolor,
                                                      objectinfo['jmag']),
                      ha='left',va='center',transform=axes.transAxes,
                      fontsize=18.0)
        elif 'jmag' in objectinfo and objectinfo['jmag']:
            axes.text(0.05,0.83,
                      '$J$ = %.3f' % (objectinfo['jmag'],),
                      ha='left',va='center',transform=axes.transAxes,
                      fontsize=18.0)

        if jkcolor:
            axes.text(0.05,0.79,
                      '$J - K$ = %.3f, $K$ = %.3f' % (jkcolor,
                                                      objectinfo['kmag']),
                      ha='left',va='center',transform=axes.transAxes,
                      fontsize=18.0)
        elif 'kmag' in objectinfo and objectinfo['kmag']:
            axes.text(0.05,0.79,
                      '$K$ = %.3f' % (objectinfo['kmag'],),
                      ha='left',va='center',transform=axes.transAxes,
                      fontsize=18.0)

        if 'sdssr' in objectinfo and objectinfo['sdssr']:
            axes.text(0.05,0.75,'SDSS $r$ = %.3f' % objectinfo['sdssr'],
                      ha='left',va='center',transform=axes.transAxes,
                      fontsize=18.0)

        if ('teff' in objectinfo and 'gmag' in objectinfo and
            objectinfo['teff'] and objectinfo['gmag']):

            # gaia data available
            axes.text(0.05,0.87,
                      r'$G$ = %.1f, $T_\mathrm{eff}$ = %d' % (
                          gmag, int(teff_val)),
                      ha='left',va='center',transform=axes.transAxes,
                      fontsize=18.0)

        # add in proper motion stuff if available in objectinfo
        if ('pmra' in objectinfo and objectinfo['pmra'] and
            'pmdecl' in objectinfo and objectinfo['pmdecl']):

            pm = total_proper_motion(objectinfo['pmra'],
                                     objectinfo['pmdecl'],
                                     objectinfo['decl'])

            axes.text(0.05,0.67,r'$\mu$ = %.2f mas yr$^{-1}$' % pm,
                      ha='left',va='center',transform=axes.transAxes,
                      fontsize=18.0)

            if 'jmag' in objectinfo and objectinfo['jmag']:

                rpm = reduced_proper_motion(objectinfo['jmag'],pm)
                axes.text(0.05,0.63,'$H_J$ = %.2f' % rpm,
                          ha='left',va='center',transform=axes.transAxes,
                          fontsize=18.0)