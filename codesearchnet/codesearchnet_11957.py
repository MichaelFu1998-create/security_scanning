def _pkl_periodogram(lspinfo,
                     plotdpi=100,
                     override_pfmethod=None):
    '''This returns the periodogram plot PNG as base64, plus info as a dict.

    Parameters
    ----------

    lspinfo : dict
        This is an lspinfo dict containing results from a period-finding
        function. If it's from an astrobase period-finding function in
        periodbase, this will already be in the correct format. To use external
        period-finder results with this function, the `lspinfo` dict must be of
        the following form, with at least the keys listed below::

            {'periods': np.array of all periods searched by the period-finder,
             'lspvals': np.array of periodogram power value for each period,
             'bestperiod': a float value that is the period with the highest
                           peak in the periodogram, i.e. the most-likely actual
                           period,
             'method': a three-letter code naming the period-finder used; must
                       be one of the keys in the
                       `astrobase.periodbase.METHODLABELS` dict,
             'nbestperiods': a list of the periods corresponding to periodogram
                             peaks (`nbestlspvals` below) to annotate on the
                             periodogram plot so they can be called out
                             visually,
             'nbestlspvals': a list of the power values associated with
                             periodogram peaks to annotate on the periodogram
                             plot so they can be called out visually; should be
                             the same length as `nbestperiods` above}

        `nbestperiods` and `nbestlspvals` must have at least 5 elements each,
        e.g. describing the five 'best' (highest power) peaks in the
        periodogram.

    plotdpi : int
        The resolution in DPI of the output periodogram plot to make.

    override_pfmethod : str or None
        This is used to set a custom label for this periodogram
        method. Normally, this is taken from the 'method' key in the input
        `lspinfo` dict, but if you want to override the output method name,
        provide this as a string here. This can be useful if you have multiple
        results you want to incorporate into a checkplotdict from a single
        period-finder (e.g. if you ran BLS over several period ranges
        separately).

    Returns
    -------

    dict
        Returns a dict that contains the following items::

            {methodname: {'periods':the period array from lspinfo,
                          'lspval': the periodogram power array from lspinfo,
                          'bestperiod': the best period from lspinfo,
                          'nbestperiods': the 'nbestperiods' list from lspinfo,
                          'nbestlspvals': the 'nbestlspvals' list from lspinfo,
                          'periodogram': base64 encoded string representation of
                                         the periodogram plot}}

        The dict is returned in this format so it can be directly incorporated
        under the period-finder's label `methodname` in a checkplotdict, using
        Python's dict `update()` method.

    '''

    # get the appropriate plot ylabel
    pgramylabel = PLOTYLABELS[lspinfo['method']]

    # get the periods and lspvals from lspinfo
    periods = lspinfo['periods']
    lspvals = lspinfo['lspvals']
    bestperiod = lspinfo['bestperiod']
    nbestperiods = lspinfo['nbestperiods']
    nbestlspvals = lspinfo['nbestlspvals']

    # open the figure instance
    pgramfig = plt.figure(figsize=(7.5,4.8),dpi=plotdpi)

    # make the plot
    plt.plot(periods,lspvals)

    plt.xscale('log',basex=10)
    plt.xlabel('Period [days]')
    plt.ylabel(pgramylabel)
    plottitle = '%s - %.6f d' % (METHODLABELS[lspinfo['method']],
                                 bestperiod)
    plt.title(plottitle)

    # show the best five peaks on the plot
    for xbestperiod, xbestpeak in zip(nbestperiods,
                                      nbestlspvals):
        plt.annotate('%.6f' % xbestperiod,
                     xy=(xbestperiod, xbestpeak), xycoords='data',
                     xytext=(0.0,25.0), textcoords='offset points',
                     arrowprops=dict(arrowstyle="->"),fontsize='14.0')

    # make a grid
    plt.grid(color='#a9a9a9',
             alpha=0.9,
             zorder=0,
             linewidth=1.0,
             linestyle=':')

    # this is the output instance
    pgrampng = StrIO()
    pgramfig.savefig(pgrampng,
                     # bbox_inches='tight',
                     pad_inches=0.0, format='png')
    plt.close()

    # encode the finderpng instance to base64
    pgrampng.seek(0)
    pgramb64 = base64.b64encode(pgrampng.read())

    # close the stringio buffer
    pgrampng.close()

    if not override_pfmethod:

        # this is the dict to return
        checkplotdict = {
            lspinfo['method']:{
                'periods':periods,
                'lspvals':lspvals,
                'bestperiod':bestperiod,
                'nbestperiods':nbestperiods,
                'nbestlspvals':nbestlspvals,
                'periodogram':pgramb64,
            }
        }

    else:

        # this is the dict to return
        checkplotdict = {
            override_pfmethod:{
                'periods':periods,
                'lspvals':lspvals,
                'bestperiod':bestperiod,
                'nbestperiods':nbestperiods,
                'nbestlspvals':nbestlspvals,
                'periodogram':pgramb64,
            }
        }

    return checkplotdict