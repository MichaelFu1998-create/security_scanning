def plot_periodbase_lsp(lspinfo, outfile=None, plotdpi=100):

    '''Makes a plot of periodograms obtained from `periodbase` functions.

    This takes the output dict produced by any `astrobase.periodbase`
    period-finder function or a pickle filename containing such a dict and makes
    a periodogram plot.

    Parameters
    ----------

    lspinfo : dict or str
        If lspinfo is a dict, it must be a dict produced by an
        `astrobase.periodbase` period-finder function or a dict from your own
        period-finder function or routine that is of the form below with at
        least these keys::

            {'periods': np.array of all periods searched by the period-finder,
             'lspvals': np.array of periodogram power value for each period,
             'bestperiod': a float value that is the period with the highest
                           peak in the periodogram, i.e. the most-likely actual
                           period,
             'method': a three-letter code naming the period-finder used; must
                       be one of the keys in the `METHODLABELS` dict above,
             'nbestperiods': a list of the periods corresponding to periodogram
                             peaks (`nbestlspvals` below) to annotate on the
                             periodogram plot so they can be called out
                             visually,
             'nbestlspvals': a list of the power values associated with
                             periodogram peaks to annotate on the periodogram
                             plot so they can be called out visually; should be
                             the same length as `nbestperiods` above}

        If lspinfo is a str, then it must be a path to a pickle file that
        contains a dict of the form described above.

    outfile : str or None
        If this is a str, will write the periodogram plot to the file specified
        by this string. If this is None, will write to a file called
        'lsp-plot.png' in the current working directory.

    plotdpi : int
        Sets the resolution in DPI of the output periodogram plot PNG file.

    Returns
    -------

    str
        Absolute path to the periodogram plot file created.

    '''

    # get the lspinfo from a pickle file transparently
    if isinstance(lspinfo,str) and os.path.exists(lspinfo):
        LOGINFO('loading LSP info from pickle %s' % lspinfo)
        with open(lspinfo,'rb') as infd:
            lspinfo = pickle.load(infd)

    try:

        # get the things to plot out of the data
        periods = lspinfo['periods']
        lspvals = lspinfo['lspvals']
        bestperiod = lspinfo['bestperiod']
        lspmethod = lspinfo['method']

        # make the LSP plot on the first subplot
        plt.plot(periods, lspvals)
        plt.xscale('log',basex=10)
        plt.xlabel('Period [days]')
        plt.ylabel(PLOTYLABELS[lspmethod])
        plottitle = '%s best period: %.6f d' % (METHODSHORTLABELS[lspmethod],
                                                bestperiod)
        plt.title(plottitle)

        # show the best five peaks on the plot
        for bestperiod, bestpeak in zip(lspinfo['nbestperiods'],
                                        lspinfo['nbestlspvals']):

            plt.annotate('%.6f' % bestperiod,
                         xy=(bestperiod, bestpeak), xycoords='data',
                         xytext=(0.0,25.0), textcoords='offset points',
                         arrowprops=dict(arrowstyle="->"),fontsize='x-small')

        # make a grid
        plt.grid(color='#a9a9a9',
                 alpha=0.9,
                 zorder=0,
                 linewidth=1.0,
                 linestyle=':')

        # make the figure
        if outfile and isinstance(outfile, str):

            if outfile.endswith('.png'):
                plt.savefig(outfile,bbox_inches='tight',dpi=plotdpi)
            else:
                plt.savefig(outfile,bbox_inches='tight')

            plt.close()
            return os.path.abspath(outfile)

        elif dispok:

            plt.show()
            plt.close()
            return

        else:

            LOGWARNING('no output file specified and no $DISPLAY set, '
                       'saving to lsp-plot.png in current directory')
            outfile = 'lsp-plot.png'
            plt.savefig(outfile,bbox_inches='tight',dpi=plotdpi)
            plt.close()
            return os.path.abspath(outfile)

    except Exception as e:

        LOGEXCEPTION('could not plot this LSP, appears to be empty')
        return