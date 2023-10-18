def make_combined_periodogram(pflist, outfile, addmethods=False):
    '''This just puts all of the period-finders on a single periodogram.

    This will renormalize all of the periodograms so their values lie between 0
    and 1, with values lying closer to 1 being more significant. Periodograms
    that give the same best periods will have their peaks line up together.

    Parameters
    ----------

    pflist : list of dict
        This is a list of result dicts from any of the period-finders in
        periodbase. To use your own period-finders' results here, make sure the
        result dict is of the form and has at least the keys below::

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
                             the same length as `nbestperiods` above,
             'kwargs': dict of kwargs passed to your own period-finder function}

    outfile : str
        This is the output file to write the output to. NOTE: EPS/PS won't work
        because we use alpha transparency to better distinguish between the
        various periodograms.

    addmethods : bool
        If this is True, will add all of the normalized periodograms together,
        then renormalize them to between 0 and 1. In this way, if all of the
        period-finders agree on something, it'll stand out easily. FIXME:
        implement this kwarg.

    Returns
    -------

    str
        The name of the generated plot file.

    '''

    import matplotlib.pyplot as plt

    for pf in pflist:

        if pf['method'] == 'pdm':

            plt.plot(pf['periods'],
                     np.max(pf['lspvals'])/pf['lspvals'] - 1.0,
                     label='%s P=%.5f' % (pf['method'], pf['bestperiod']),
                     alpha=0.5)

        else:

            plt.plot(pf['periods'],
                     pf['lspvals']/np.max(pf['lspvals']),
                     label='%s P=%.5f' % (pf['method'], pf['bestperiod']),
                     alpha=0.5)


    plt.xlabel('period [days]')
    plt.ylabel('normalized periodogram power')

    plt.xscale('log')
    plt.legend()
    plt.tight_layout()
    plt.savefig(outfile)
    plt.close('all')

    return outfile