def plot_periodicvar_recovery_results(
        precvar_results,
        aliases_count_as_recovered=None,
        magbins=None,
        periodbins=None,
        amplitudebins=None,
        ndetbins=None,
        minbinsize=1,
        plotfile_ext='png',
):
    '''This plots the results of periodic var recovery.

    This function makes plots for periodicvar recovered fraction as a function
    of:

    - magbin
    - periodbin
    - amplitude of variability
    - ndet

    with plot lines broken down by:

    - magcol
    - periodfinder
    - vartype
    - recovery status

    The kwargs `magbins`, `periodbins`, `amplitudebins`, and `ndetbins` can be
    used to set the bin lists as needed. The kwarg `minbinsize` controls how
    many elements per bin are required to accept a bin in processing its
    recovery characteristics for mags, periods, amplitudes, and ndets.

    Parameters
    ----------

    precvar_results : dict or str
        This is either a dict returned by parallel_periodicvar_recovery or the
        pickle created by that function.

    aliases_count_as_recovered : list of str or 'all'
        This is used to set which kinds of aliases this function considers as
        'recovered' objects. Normally, we require that recovered objects have a
        recovery status of 'actual' to indicate the actual period was
        recovered. To change this default behavior, aliases_count_as_recovered
        can be set to a list of alias status strings that should be considered
        as 'recovered' objects as well. Choose from the following alias types::

          'twice'                    recovered_p = 2.0*actual_p
          'half'                     recovered_p = 0.5*actual_p
          'ratio_over_1plus'         recovered_p = actual_p/(1.0+actual_p)
          'ratio_over_1minus'        recovered_p = actual_p/(1.0-actual_p)
          'ratio_over_1plus_twice'   recovered_p = actual_p/(1.0+2.0*actual_p)
          'ratio_over_1minus_twice'  recovered_p = actual_p/(1.0-2.0*actual_p)
          'ratio_over_1plus_thrice'  recovered_p = actual_p/(1.0+3.0*actual_p)
          'ratio_over_1minus_thrice' recovered_p = actual_p/(1.0-3.0*actual_p)
          'ratio_over_minus1'        recovered_p = actual_p/(actual_p - 1.0)
          'ratio_over_twice_minus1'  recovered_p = actual_p/(2.0*actual_p - 1.0)

        or set `aliases_count_as_recovered='all'` to include all of the above in
        the 'recovered' periodic var list.

    magbins : np.array
        The magnitude bins to plot the recovery rate results over. If None, the
        default mag bins will be used: `np.arange(8.0,16.25,0.25)`.

    periodbins : np.array
        The period bins to plot the recovery rate results over. If None, the
        default period bins will be used: `np.arange(0.0,500.0,0.5)`.

    amplitudebins : np.array
        The variability amplitude bins to plot the recovery rate results
        over. If None, the default amplitude bins will be used:
        `np.arange(0.0,2.0,0.05)`.

    ndetbins : np.array
        The ndet bins to plot the recovery rate results over. If None, the
        default ndet bins will be used: `np.arange(0.0,60000.0,1000.0)`.

    minbinsize : int
        The minimum number of objects per bin required to plot a bin and its
        recovery fraction on the plot.

    plotfile_ext : {'png','pdf'}
        Sets the plot output files' extension.

    Returns
    -------

    dict
        A dict containing recovery fraction statistics and the paths to each of
        the plots made.

    '''

    # get the result pickle/dict
    if isinstance(precvar_results, str) and os.path.exists(precvar_results):

        with open(precvar_results,'rb') as infd:
            precvar = pickle.load(infd)

    elif isinstance(precvar_results, dict):

        precvar = precvar_results

    else:
        LOGERROR('could not understand the input '
                 'periodic var recovery dict/pickle')
        return None

    # get the simbasedir and open the fakelc-info.pkl. we'll need the magbins
    # definition from here.
    simbasedir = precvar['simbasedir']

    lcinfof = os.path.join(simbasedir,'fakelcs-info.pkl')

    if not os.path.exists(lcinfof):
        LOGERROR('fakelcs-info.pkl does not exist in %s, can\'t continue' %
                 simbasedir)
        return None

    with open(lcinfof,'rb') as infd:
        lcinfo = pickle.load(infd)

    # get the magcols, vartypes, sdssr, isvariable flags
    magcols = lcinfo['magcols']
    objectid = lcinfo['objectid']
    ndet = lcinfo['ndet']
    sdssr = lcinfo['sdssr']

    # get the actual periodic vars
    actual_periodicvars = precvar['actual_periodicvars']

    # generate lists of objects binned by magbins and periodbins
    LOGINFO('getting sdssr and ndet for actual periodic vars...')

    # get the sdssr and ndet for all periodic vars
    periodicvar_sdssr = []
    periodicvar_ndet = []
    periodicvar_objectids = []

    for pobj in actual_periodicvars:

        pobjind = objectid == pobj
        periodicvar_objectids.append(pobj)
        periodicvar_sdssr.append(sdssr[pobjind])
        periodicvar_ndet.append(ndet[pobjind])


    periodicvar_sdssr = np.array(periodicvar_sdssr)
    periodicvar_objectids = np.array(periodicvar_objectids)
    periodicvar_ndet = np.array(periodicvar_ndet)

    LOGINFO('getting periods, vartypes, '
            'amplitudes, ndet for actual periodic vars...')

    # get the periods, vartypes, amplitudes for the actual periodic vars
    periodicvar_periods = [
        np.asscalar(precvar['details'][x]['actual_varperiod'])
        for x in periodicvar_objectids
    ]
    periodicvar_amplitudes = [
        np.asscalar(precvar['details'][x]['actual_varamplitude'])
        for x in periodicvar_objectids
    ]
    periodicvar_vartypes = [
        precvar['details'][x]['actual_vartype'] for x in periodicvar_objectids
    ]

    #
    # do the binning
    #

    # bin by mag
    LOGINFO('binning actual periodic vars by magnitude...')

    magbinned_sdssr = []
    magbinned_periodicvars = []

    if not magbins:
        magbins = PERIODREC_DEFAULT_MAGBINS
    magbininds = np.digitize(np.ravel(periodicvar_sdssr), magbins)

    for mbinind, magi in zip(np.unique(magbininds),
                             range(len(magbins)-1)):

        thisbin_periodicvars = periodicvar_objectids[magbininds == mbinind]

        if (thisbin_periodicvars.size > (minbinsize-1)):

            magbinned_sdssr.append((magbins[magi] + magbins[magi+1])/2.0)
            magbinned_periodicvars.append(thisbin_periodicvars)


    # bin by period
    LOGINFO('binning actual periodic vars by period...')

    periodbinned_periods = []
    periodbinned_periodicvars = []

    if not periodbins:
        periodbins = PERIODREC_DEFAULT_PERIODBINS
    periodbininds = np.digitize(np.ravel(periodicvar_periods), periodbins)

    for pbinind, peri in zip(np.unique(periodbininds),
                             range(len(periodbins)-1)):

        thisbin_periodicvars = periodicvar_objectids[periodbininds == pbinind]

        if (thisbin_periodicvars.size > (minbinsize-1)):

            periodbinned_periods.append((periodbins[peri] +
                                         periodbins[peri+1])/2.0)
            periodbinned_periodicvars.append(thisbin_periodicvars)


    # bin by amplitude of variability
    LOGINFO('binning actual periodic vars by variability amplitude...')

    amplitudebinned_amplitudes = []
    amplitudebinned_periodicvars = []

    if not amplitudebins:
        amplitudebins = PERIODREC_DEFAULT_AMPBINS
    amplitudebininds = np.digitize(np.ravel(np.abs(periodicvar_amplitudes)),
                                   amplitudebins)

    for abinind, ampi in zip(np.unique(amplitudebininds),
                             range(len(amplitudebins)-1)):

        thisbin_periodicvars = periodicvar_objectids[
            amplitudebininds == abinind
        ]

        if (thisbin_periodicvars.size > (minbinsize-1)):

            amplitudebinned_amplitudes.append(
                (amplitudebins[ampi] +
                 amplitudebins[ampi+1])/2.0
            )
            amplitudebinned_periodicvars.append(thisbin_periodicvars)


    # bin by ndet
    LOGINFO('binning actual periodic vars by ndet...')

    ndetbinned_ndets = []
    ndetbinned_periodicvars = []

    if not ndetbins:
        ndetbins = PERIODREC_DEFAULT_NDETBINS
    ndetbininds = np.digitize(np.ravel(periodicvar_ndet), ndetbins)

    for nbinind, ndeti in zip(np.unique(ndetbininds),
                              range(len(ndetbins)-1)):

        thisbin_periodicvars = periodicvar_objectids[ndetbininds == nbinind]

        if (thisbin_periodicvars.size > (minbinsize-1)):

            ndetbinned_ndets.append(
                (ndetbins[ndeti] +
                 ndetbins[ndeti+1])/2.0
            )
            ndetbinned_periodicvars.append(thisbin_periodicvars)


    # now figure out what 'recovered' means using the provided
    # aliases_count_as_recovered kwarg
    recovered_status = ['actual']

    if isinstance(aliases_count_as_recovered, list):

        for atype in aliases_count_as_recovered:
            if atype in ALIAS_TYPES:
                recovered_status.append(atype)
            else:
                LOGWARNING('unknown alias type: %s, skipping' % atype)

    elif aliases_count_as_recovered and aliases_count_as_recovered == 'all':
        for atype in ALIAS_TYPES[1:]:
            recovered_status.append(atype)

    # find all the matching objects for these recovered statuses
    recovered_periodicvars = np.array(
        [precvar['details'][x]['objectid'] for x in precvar['details']
         if (precvar['details'][x] is not None and
             precvar['details'][x]['best_recovered_status']
             in recovered_status)],
        dtype=np.unicode_
    )

    LOGINFO('recovered %s/%s periodic variables (frac: %.3f) with '
            'period recovery status: %s' %
            (recovered_periodicvars.size,
             actual_periodicvars.size,
             float(recovered_periodicvars.size/actual_periodicvars.size),
             ', '.join(recovered_status)))


    # get the objects recovered per bin and overall recovery fractions per bin
    magbinned_recovered_objects = [
        np.intersect1d(x,recovered_periodicvars)
        for x in magbinned_periodicvars
    ]
    magbinned_recfrac = np.array([float(x.size/y.size) for x,y
                                  in zip(magbinned_recovered_objects,
                                         magbinned_periodicvars)])

    periodbinned_recovered_objects = [
        np.intersect1d(x,recovered_periodicvars)
        for x in periodbinned_periodicvars
    ]
    periodbinned_recfrac = np.array([float(x.size/y.size) for x,y
                                     in zip(periodbinned_recovered_objects,
                                            periodbinned_periodicvars)])

    amplitudebinned_recovered_objects = [
        np.intersect1d(x,recovered_periodicvars)
        for x in amplitudebinned_periodicvars
    ]
    amplitudebinned_recfrac = np.array(
        [float(x.size/y.size) for x,y
         in zip(amplitudebinned_recovered_objects,
                amplitudebinned_periodicvars)]
    )

    ndetbinned_recovered_objects = [
        np.intersect1d(x,recovered_periodicvars)
        for x in ndetbinned_periodicvars
    ]
    ndetbinned_recfrac = np.array([float(x.size/y.size) for x,y
                                   in zip(ndetbinned_recovered_objects,
                                          ndetbinned_periodicvars)])


    # convert the bin medians to arrays
    magbinned_sdssr = np.array(magbinned_sdssr)
    periodbinned_periods = np.array(periodbinned_periods)
    amplitudebinned_amplitudes = np.array(amplitudebinned_amplitudes)
    ndetbinned_ndets = np.array(ndetbinned_ndets)

    # this is the initial output dict
    outdict = {
        'simbasedir':simbasedir,
        'precvar_results':precvar,
        'magcols':magcols,
        'objectids':objectid,
        'ndet':ndet,
        'sdssr':sdssr,
        'actual_periodicvars':actual_periodicvars,
        'recovered_periodicvars':recovered_periodicvars,
        'recovery_definition':recovered_status,
        # mag binned actual periodicvars
        # note that only bins with nobjects > minbinsize are included
        'magbins':magbins,
        'magbinned_mags':magbinned_sdssr,
        'magbinned_periodicvars':magbinned_periodicvars,
        'magbinned_recoveredvars':magbinned_recovered_objects,
        'magbinned_recfrac':magbinned_recfrac,
        # period binned actual periodicvars
        # note that only bins with nobjects > minbinsize are included
        'periodbins':periodbins,
        'periodbinned_periods':periodbinned_periods,
        'periodbinned_periodicvars':periodbinned_periodicvars,
        'periodbinned_recoveredvars':periodbinned_recovered_objects,
        'periodbinned_recfrac':periodbinned_recfrac,
        # amplitude binned actual periodicvars
        # note that only bins with nobjects > minbinsize are included
        'amplitudebins':amplitudebins,
        'amplitudebinned_amplitudes':amplitudebinned_amplitudes,
        'amplitudebinned_periodicvars':amplitudebinned_periodicvars,
        'amplitudebinned_recoveredvars':amplitudebinned_recovered_objects,
        'amplitudebinned_recfrac':amplitudebinned_recfrac,
        # ndet binned actual periodicvars
        # note that only bins with nobjects > minbinsize are included
        'ndetbins':ndetbins,
        'ndetbinned_ndets':ndetbinned_ndets,
        'ndetbinned_periodicvars':ndetbinned_periodicvars,
        'ndetbinned_recoveredvars':ndetbinned_recovered_objects,
        'ndetbinned_recfrac':ndetbinned_recfrac,
    }


    # figure out which pfmethods were used
    all_pfmethods = np.unique(
        np.concatenate(
            [np.unique(precvar['details'][x]['recovery_pfmethods'])
             for x in precvar['details']]
        )
    )

    # figure out all vartypes
    all_vartypes = np.unique(
        [(precvar['details'][x]['actual_vartype'])
         for x in precvar['details'] if
         (precvar['details'][x]['actual_vartype'] is not None)]
    )

    # figure out all alias types
    all_aliastypes = recovered_status

    # add these to the outdict
    outdict['aliastypes'] = all_aliastypes
    outdict['pfmethods'] = all_pfmethods
    outdict['vartypes'] = all_vartypes


    # these are recfracs per-magcol, -vartype, -periodfinder, -aliastype
    # binned appropriately by mags, periods, amplitudes, and ndet
    # all of these have the shape as the magcols, aliastypes, pfmethods, and
    # vartypes lists above.

    magbinned_per_magcol_recfracs = []
    magbinned_per_vartype_recfracs = []
    magbinned_per_pfmethod_recfracs = []
    magbinned_per_aliastype_recfracs = []

    periodbinned_per_magcol_recfracs = []
    periodbinned_per_vartype_recfracs = []
    periodbinned_per_pfmethod_recfracs = []
    periodbinned_per_aliastype_recfracs = []

    amplitudebinned_per_magcol_recfracs = []
    amplitudebinned_per_vartype_recfracs = []
    amplitudebinned_per_pfmethod_recfracs = []
    amplitudebinned_per_aliastype_recfracs = []

    ndetbinned_per_magcol_recfracs = []
    ndetbinned_per_vartype_recfracs = []
    ndetbinned_per_pfmethod_recfracs = []
    ndetbinned_per_aliastype_recfracs = []


    #
    # finally, we do stuff for the plots!
    #
    recplotdir = os.path.join(simbasedir, 'periodic-variable-recovery-plots')
    if not os.path.exists(recplotdir):
        os.mkdir(recplotdir)

    # 1. recovery-rate by magbin

    # 1a. plot of overall recovery rate per magbin
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    plt.plot(magbinned_sdssr, magbinned_recfrac,marker='.',ms=0.0)
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('overall recovery fraction by periodic var magnitudes')
    plt.ylim((0,1))
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-magnitudes-overall.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 1b. plot of recovery rate per magbin per magcol
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    for magcol in magcols:

        thismagcol_recfracs = []

        for magbin_pv, magbin_rv in zip(magbinned_periodicvars,
                                        magbinned_recovered_objects):

            thisbin_thismagcol_recvars = [
                x for x in magbin_rv
                if (precvar['details'][x]['best_recovered_magcol'] == magcol)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thismagcol_recvars).size /
                magbin_pv.size
            )
            thismagcol_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(magbinned_sdssr,
                 np.array(thismagcol_recfracs),
                 marker='.',
                 label='magcol: %s' % magcol,
                 ms=0.0)

        # add this to the outdict array
        magbinned_per_magcol_recfracs.append(np.array(thismagcol_recfracs))

    # finish up the plot
    plt.plot(magbinned_sdssr, magbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per magcol recovery fraction by periodic var magnitudes')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-magnitudes-magcols.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 1c. plot of recovery rate per magbin per periodfinder
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out which pfmethods were used
    all_pfmethods = np.unique(
        np.concatenate(
            [np.unique(precvar['details'][x]['recovery_pfmethods'])
             for x in precvar['details']]
        )
    )

    for pfm in all_pfmethods:

        thispf_recfracs = []

        for magbin_pv, magbin_rv in zip(magbinned_periodicvars,
                                        magbinned_recovered_objects):

            thisbin_thispf_recvars = [
                x for x in magbin_rv
                if (precvar['details'][x]['best_recovered_pfmethod'] == pfm)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thispf_recvars).size /
                magbin_pv.size
            )
            thispf_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(magbinned_sdssr,
                 np.array(thispf_recfracs),
                 marker='.',
                 label='%s' % pfm.upper(),
                 ms=0.0)

        # add this to the outdict array
        magbinned_per_pfmethod_recfracs.append(np.array(thispf_recfracs))

    # finish up the plot
    plt.plot(magbinned_sdssr, magbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per period-finder recovery fraction by periodic var magnitudes')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-magnitudes-pfmethod.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 1d. plot of recovery rate per magbin per variable type
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out all vartypes
    all_vartypes = np.unique(
        [(precvar['details'][x]['actual_vartype'])
         for x in precvar['details'] if
         (precvar['details'][x]['actual_vartype'] is not None)]
    )

    for vt in all_vartypes:

        thisvt_recfracs = []

        for magbin_pv, magbin_rv in zip(magbinned_periodicvars,
                                        magbinned_recovered_objects):

            thisbin_thisvt_recvars = [
                x for x in magbin_rv
                if (precvar['details'][x]['actual_vartype'] == vt)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thisvt_recvars).size /
                magbin_pv.size
            )
            thisvt_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(magbinned_sdssr,
                 np.array(thisvt_recfracs),
                 marker='.',
                 label='%s' % vt,
                 ms=0.0)

        # add this to the outdict array
        magbinned_per_vartype_recfracs.append(np.array(thisvt_recfracs))

    # finish up the plot
    plt.plot(magbinned_sdssr, magbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per vartype recovery fraction by periodic var magnitudes')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-magnitudes-vartype.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 1e. plot of recovery rate per magbin per alias type
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out all alias types
    all_aliastypes = recovered_status

    for at in all_aliastypes:

        thisat_recfracs = []

        for magbin_pv, magbin_rv in zip(magbinned_periodicvars,
                                        magbinned_recovered_objects):

            thisbin_thisat_recvars = [
                x for x in magbin_rv
                if (precvar['details'][x]['best_recovered_status'][0] == at)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thisat_recvars).size /
                magbin_pv.size
            )
            thisat_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(magbinned_sdssr,
                 np.array(thisat_recfracs),
                 marker='.',
                 label='%s' % at,
                 ms=0.0)

        # add this to the outdict array
        magbinned_per_aliastype_recfracs.append(np.array(thisat_recfracs))

    # finish up the plot
    plt.plot(magbinned_sdssr, magbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per alias-type recovery fraction by periodic var magnitudes')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-magnitudes-aliastype.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 2. recovery-rate by periodbin

    # 2a. plot of overall recovery rate per periodbin
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    plt.plot(periodbinned_periods, periodbinned_recfrac,
             marker='.',ms=0.0)
    plt.xlabel('periodic variable period [days]')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('overall recovery fraction by periodic var periods')
    plt.ylim((0,1))
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-periods-overall.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')

    # 2b. plot of recovery rate per periodbin per magcol
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    for magcol in magcols:

        thismagcol_recfracs = []

        for periodbin_pv, periodbin_rv in zip(periodbinned_periodicvars,
                                              periodbinned_recovered_objects):

            thisbin_thismagcol_recvars = [
                x for x in periodbin_rv
                if (precvar['details'][x]['best_recovered_magcol'] == magcol)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thismagcol_recvars).size /
                periodbin_pv.size
            )
            thismagcol_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(periodbinned_periods,
                 np.array(thismagcol_recfracs),
                 marker='.',
                 label='magcol: %s' % magcol,
                 ms=0.0)

        # add this to the outdict array
        periodbinned_per_magcol_recfracs.append(np.array(thismagcol_recfracs))

    # finish up the plot
    plt.plot(periodbinned_periods, periodbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per magcol recovery fraction by periodic var periods')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-periods-magcols.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 2c. plot of recovery rate per periodbin per periodfinder
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out which pfmethods were used
    all_pfmethods = np.unique(
        np.concatenate(
            [np.unique(precvar['details'][x]['recovery_pfmethods'])
             for x in precvar['details']]
        )
    )

    for pfm in all_pfmethods:

        thispf_recfracs = []

        for periodbin_pv, periodbin_rv in zip(periodbinned_periodicvars,
                                              periodbinned_recovered_objects):

            thisbin_thispf_recvars = [
                x for x in periodbin_rv
                if (precvar['details'][x]['best_recovered_pfmethod'] == pfm)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thispf_recvars).size /
                periodbin_pv.size
            )
            thispf_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(periodbinned_periods,
                 np.array(thispf_recfracs),
                 marker='.',
                 label='%s' % pfm.upper(),
                 ms=0.0)

        # add this to the outdict array
        periodbinned_per_pfmethod_recfracs.append(np.array(thispf_recfracs))

    # finish up the plot
    plt.plot(periodbinned_periods, periodbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per period-finder recovery fraction by periodic var periods')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-periods-pfmethod.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 2d. plot of recovery rate per periodbin per variable type
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out all vartypes
    all_vartypes = np.unique(
        [(precvar['details'][x]['actual_vartype'])
         for x in precvar['details'] if
         (precvar['details'][x]['actual_vartype'] is not None)]
    )

    for vt in all_vartypes:

        thisvt_recfracs = []

        for periodbin_pv, periodbin_rv in zip(periodbinned_periodicvars,
                                              periodbinned_recovered_objects):

            thisbin_thisvt_recvars = [
                x for x in periodbin_rv
                if (precvar['details'][x]['actual_vartype'] == vt)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thisvt_recvars).size /
                periodbin_pv.size
            )
            thisvt_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(periodbinned_periods,
                 np.array(thisvt_recfracs),
                 marker='.',
                 label='%s' % vt,
                 ms=0.0)

        # add this to the outdict array
        periodbinned_per_vartype_recfracs.append(np.array(thisvt_recfracs))

    # finish up the plot
    plt.plot(periodbinned_periods, periodbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per vartype recovery fraction by periodic var magnitudes')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-periods-vartype.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 2e. plot of recovery rate per periodbin per alias type
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out all vartypes
    all_aliastypes = recovered_status

    for at in all_aliastypes:

        thisat_recfracs = []

        for periodbin_pv, periodbin_rv in zip(
                periodbinned_periodicvars,
                periodbinned_recovered_objects
        ):

            thisbin_thisat_recvars = [
                x for x in periodbin_rv
                if (precvar['details'][x]['best_recovered_status'][0] == at)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thisat_recvars).size /
                periodbin_pv.size
            )
            thisat_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(periodbinned_periods,
                 np.array(thisat_recfracs),
                 marker='.',
                 label='%s' % at,
                 ms=0.0)

        # add this to the outdict array
        periodbinned_per_aliastype_recfracs.append(np.array(thisat_recfracs))

    # finish up the plot
    plt.plot(periodbinned_periods, periodbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per alias-type recovery fraction by periodic var magnitudes')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-periods-aliastype.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 3. recovery-rate by amplitude bin

    # 3a. plot of overall recovery rate per amplitude bin
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    plt.plot(amplitudebinned_amplitudes, amplitudebinned_recfrac,
             marker='.',ms=0.0)
    plt.xlabel('periodic variable amplitude [mag]')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('overall recovery fraction by periodic var amplitudes')
    plt.ylim((0,1))
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-amplitudes-overall.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')

    # 3b. plot of recovery rate per amplitude bin per magcol
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    for magcol in magcols:

        thismagcol_recfracs = []

        for amplitudebin_pv, amplitudebin_rv in zip(
                amplitudebinned_periodicvars,
                amplitudebinned_recovered_objects
        ):

            thisbin_thismagcol_recvars = [
                x for x in amplitudebin_rv
                if (precvar['details'][x]['best_recovered_magcol'] == magcol)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thismagcol_recvars).size /
                amplitudebin_pv.size
            )
            thismagcol_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(amplitudebinned_amplitudes,
                 np.array(thismagcol_recfracs),
                 marker='.',
                 label='magcol: %s' % magcol,
                 ms=0.0)

        # add this to the outdict array
        amplitudebinned_per_magcol_recfracs.append(
            np.array(thismagcol_recfracs)
        )

    # finish up the plot
    plt.plot(amplitudebinned_amplitudes, amplitudebinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per magcol recovery fraction by periodic var amplitudes')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-amplitudes-magcols.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 3c. plot of recovery rate per amplitude bin per periodfinder
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out which pfmethods were used
    all_pfmethods = np.unique(
        np.concatenate(
            [np.unique(precvar['details'][x]['recovery_pfmethods'])
             for x in precvar['details']]
        )
    )

    for pfm in all_pfmethods:

        thispf_recfracs = []

        for amplitudebin_pv, amplitudebin_rv in zip(
                amplitudebinned_periodicvars,
                amplitudebinned_recovered_objects
        ):

            thisbin_thispf_recvars = [
                x for x in amplitudebin_rv
                if (precvar['details'][x]['best_recovered_pfmethod'] == pfm)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thispf_recvars).size /
                amplitudebin_pv.size
            )
            thispf_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(amplitudebinned_amplitudes,
                 np.array(thispf_recfracs),
                 marker='.',
                 label='%s' % pfm.upper(),
                 ms=0.0)

        # add this to the outdict array
        amplitudebinned_per_pfmethod_recfracs.append(
            np.array(thispf_recfracs)
        )

    # finish up the plot
    plt.plot(amplitudebinned_amplitudes, amplitudebinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per period-finder recovery fraction by periodic var amplitudes')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-amplitudes-pfmethod.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 3d. plot of recovery rate per amplitude bin per variable type
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out all vartypes
    all_vartypes = np.unique(
        [(precvar['details'][x]['actual_vartype'])
         for x in precvar['details'] if
         (precvar['details'][x]['actual_vartype'] is not None)]
    )

    for vt in all_vartypes:

        thisvt_recfracs = []

        for amplitudebin_pv, amplitudebin_rv in zip(
                amplitudebinned_periodicvars,
                amplitudebinned_recovered_objects
        ):

            thisbin_thisvt_recvars = [
                x for x in amplitudebin_rv
                if (precvar['details'][x]['actual_vartype'] == vt)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thisvt_recvars).size /
                amplitudebin_pv.size
            )
            thisvt_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(amplitudebinned_amplitudes,
                 np.array(thisvt_recfracs),
                 marker='.',
                 label='%s' % vt,
                 ms=0.0)

        # add this to the outdict array
        amplitudebinned_per_vartype_recfracs.append(
            np.array(thisvt_recfracs)
        )


    # finish up the plot
    plt.plot(amplitudebinned_amplitudes, amplitudebinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per vartype recovery fraction by periodic var amplitudes')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-amplitudes-vartype.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 3e. plot of recovery rate per amplitude bin per alias type
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out all vartypes
    all_aliastypes = recovered_status

    for at in all_aliastypes:

        thisat_recfracs = []

        for amplitudebin_pv, amplitudebin_rv in zip(
                amplitudebinned_periodicvars,
                amplitudebinned_recovered_objects
        ):

            thisbin_thisat_recvars = [
                x for x in amplitudebin_rv
                if (precvar['details'][x]['best_recovered_status'][0] == at)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thisat_recvars).size /
                amplitudebin_pv.size
            )
            thisat_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(amplitudebinned_amplitudes,
                 np.array(thisat_recfracs),
                 marker='.',
                 label='%s' % at,
                 ms=0.0)

        # add this to the outdict array
        amplitudebinned_per_aliastype_recfracs.append(
            np.array(thisat_recfracs)
        )


    # finish up the plot
    plt.plot(amplitudebinned_amplitudes, amplitudebinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per alias-type recovery fraction by periodic var amplitudes')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-amplitudes-aliastype.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 4. recovery-rate by ndet bin

    # 4a. plot of overall recovery rate per ndet bin
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    plt.plot(ndetbinned_ndets, ndetbinned_recfrac,
             marker='.',ms=0.0)
    plt.xlabel('periodic variable light curve points')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('overall recovery fraction by periodic var ndet')
    plt.ylim((0,1))
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-ndet-overall.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')

    # 4b. plot of recovery rate per ndet bin per magcol
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    for magcol in magcols:

        thismagcol_recfracs = []

        for ndetbin_pv, ndetbin_rv in zip(ndetbinned_periodicvars,
                                          ndetbinned_recovered_objects):

            thisbin_thismagcol_recvars = [
                x for x in ndetbin_rv
                if (precvar['details'][x]['best_recovered_magcol'] == magcol)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thismagcol_recvars).size /
                ndetbin_pv.size
            )
            thismagcol_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(ndetbinned_ndets,
                 np.array(thismagcol_recfracs),
                 marker='.',
                 label='magcol: %s' % magcol,
                 ms=0.0)

        # add this to the outdict array
        ndetbinned_per_magcol_recfracs.append(
            np.array(thismagcol_recfracs)
        )

    # finish up the plot
    plt.plot(ndetbinned_ndets, ndetbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per magcol recovery fraction by periodic var ndets')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-ndet-magcols.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 4c. plot of recovery rate per ndet bin per periodfinder
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out which pfmethods were used
    all_pfmethods = np.unique(
        np.concatenate(
            [np.unique(precvar['details'][x]['recovery_pfmethods'])
             for x in precvar['details']]
        )
    )

    for pfm in all_pfmethods:

        thispf_recfracs = []

        for ndetbin_pv, ndetbin_rv in zip(ndetbinned_periodicvars,
                                          ndetbinned_recovered_objects):

            thisbin_thispf_recvars = [
                x for x in ndetbin_rv
                if (precvar['details'][x]['best_recovered_pfmethod'] == pfm)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thispf_recvars).size /
                ndetbin_pv.size
            )
            thispf_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(ndetbinned_ndets,
                 np.array(thispf_recfracs),
                 marker='.',
                 label='%s' % pfm.upper(),
                 ms=0.0)

        # add this to the outdict array
        ndetbinned_per_pfmethod_recfracs.append(
            np.array(thispf_recfracs)
        )

    # finish up the plot
    plt.plot(ndetbinned_ndets, ndetbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per period-finder recovery fraction by periodic var ndets')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-ndet-pfmethod.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 4d. plot of recovery rate per ndet bin per variable type
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out all vartypes
    all_vartypes = np.unique(
        [(precvar['details'][x]['actual_vartype'])
         for x in precvar['details'] if
         (precvar['details'][x]['actual_vartype'] in PERIODIC_VARTYPES)]
    )

    for vt in all_vartypes:

        thisvt_recfracs = []

        for ndetbin_pv, ndetbin_rv in zip(ndetbinned_periodicvars,
                                          ndetbinned_recovered_objects):

            thisbin_thisvt_recvars = [
                x for x in ndetbin_rv
                if (precvar['details'][x]['actual_vartype'] == vt)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thisvt_recvars).size /
                ndetbin_pv.size
            )
            thisvt_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(ndetbinned_ndets,
                 np.array(thisvt_recfracs),
                 marker='.',
                 label='%s' % vt,
                 ms=0.0)

        # add this to the outdict array
        ndetbinned_per_vartype_recfracs.append(
            np.array(thisvt_recfracs)
        )

    # finish up the plot
    plt.plot(ndetbinned_ndets, ndetbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per vartype recovery fraction by periodic var ndets')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-ndet-vartype.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')

    # 4e. plot of recovery rate per ndet bin per alias type
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    # figure out all vartypes
    all_aliastypes = recovered_status

    for at in all_aliastypes:

        thisat_recfracs = []

        for ndetbin_pv, ndetbin_rv in zip(ndetbinned_periodicvars,
                                          ndetbinned_recovered_objects):

            thisbin_thisat_recvars = [
                x for x in ndetbin_rv
                if (precvar['details'][x]['best_recovered_status'][0] == at)
            ]
            thisbin_thismagcol_recfrac = (
                np.array(thisbin_thisat_recvars).size /
                ndetbin_pv.size
            )
            thisat_recfracs.append(thisbin_thismagcol_recfrac)

        # now that we have per magcol recfracs, plot them
        plt.plot(ndetbinned_ndets,
                 np.array(thisat_recfracs),
                 marker='.',
                 label='%s' % at,
                 ms=0.0)

        # add this to the outdict array
        ndetbinned_per_aliastype_recfracs.append(
            np.array(thisat_recfracs)
        )

    # finish up the plot
    plt.plot(ndetbinned_ndets, ndetbinned_recfrac,
             marker='.',ms=0.0, label='overall', color='k')
    plt.xlabel(r'SDSS $r$ magnitude')
    plt.ylabel('recovered fraction of periodic variables')
    plt.title('per alias-type recovery fraction by periodic var ndets')
    plt.ylim((0,1))
    plt.legend(markerscale=10.0)
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-binned-ndet-aliastype.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')

    # update the lists in the outdict
    outdict['magbinned_per_magcol_recfracs'] = (
        magbinned_per_magcol_recfracs
    )
    outdict['magbinned_per_pfmethod_recfracs'] = (
        magbinned_per_pfmethod_recfracs
    )
    outdict['magbinned_per_vartype_recfracs'] = (
        magbinned_per_vartype_recfracs
    )
    outdict['magbinned_per_aliastype_recfracs'] = (
        magbinned_per_aliastype_recfracs
    )

    outdict['periodbinned_per_magcol_recfracs'] = (
        periodbinned_per_magcol_recfracs
    )
    outdict['periodbinned_per_pfmethod_recfracs'] = (
        periodbinned_per_pfmethod_recfracs
    )
    outdict['periodbinned_per_vartype_recfracs'] = (
        periodbinned_per_vartype_recfracs
    )
    outdict['periodbinned_per_aliastype_recfracs'] = (
        periodbinned_per_aliastype_recfracs
    )

    outdict['amplitudebinned_per_magcol_recfracs'] = (
        amplitudebinned_per_magcol_recfracs
    )
    outdict['amplitudebinned_per_pfmethod_recfracs'] = (
        amplitudebinned_per_pfmethod_recfracs
    )
    outdict['amplitudebinned_per_vartype_recfracs'] = (
        amplitudebinned_per_vartype_recfracs
    )
    outdict['amplitudebinned_per_aliastype_recfracs'] = (
        amplitudebinned_per_aliastype_recfracs
    )

    outdict['ndetbinned_per_magcol_recfracs'] = (
        ndetbinned_per_magcol_recfracs
    )
    outdict['ndetbinned_per_pfmethod_recfracs'] = (
        ndetbinned_per_pfmethod_recfracs
    )
    outdict['ndetbinned_per_vartype_recfracs'] = (
        ndetbinned_per_vartype_recfracs
    )
    outdict['ndetbinned_per_aliastype_recfracs'] = (
        ndetbinned_per_aliastype_recfracs
    )


    # get the overall recovered vars per pfmethod
    overall_recvars_per_pfmethod = []

    for pfm in all_pfmethods:

        thispfm_recvars = np.array([
            x for x in precvar['details'] if
            ((x in recovered_periodicvars) and
             (precvar['details'][x]['best_recovered_pfmethod'] == pfm))
        ])
        overall_recvars_per_pfmethod.append(thispfm_recvars)


    # get the overall recovered vars per vartype
    overall_recvars_per_vartype = []

    for vt in all_vartypes:

        thisvt_recvars = np.array([
            x for x in precvar['details'] if
            ((x in recovered_periodicvars) and
             (precvar['details'][x]['actual_vartype'] == vt))
        ])
        overall_recvars_per_vartype.append(thisvt_recvars)


    # get the overall recovered vars per magcol
    overall_recvars_per_magcol = []

    for mc in magcols:

        thismc_recvars = np.array([
            x for x in precvar['details'] if
            ((x in recovered_periodicvars) and
             (precvar['details'][x]['best_recovered_magcol'] == mc))
        ])
        overall_recvars_per_magcol.append(thismc_recvars)


    # get the overall recovered vars per aliastype
    overall_recvars_per_aliastype = []

    for at in all_aliastypes:

        thisat_recvars = np.array([
            x for x in precvar['details'] if
            ((x in recovered_periodicvars) and
             (precvar['details'][x]['best_recovered_status'] == at))
        ])
        overall_recvars_per_aliastype.append(thisat_recvars)

    # update the outdict with these
    outdict['overall_recfrac_per_pfmethod'] = np.array([
        x.size/actual_periodicvars.size for x in overall_recvars_per_pfmethod
    ])
    outdict['overall_recfrac_per_vartype'] = np.array([
        x.size/actual_periodicvars.size for x in overall_recvars_per_vartype
    ])
    outdict['overall_recfrac_per_magcol'] = np.array([
        x.size/actual_periodicvars.size for x in overall_recvars_per_magcol
    ])
    outdict['overall_recfrac_per_aliastype'] = np.array([
        x.size/actual_periodicvars.size for x in overall_recvars_per_aliastype
    ])


    # 5. bar plot of overall recovery rate per pfmethod
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    xt = np.arange(len(all_pfmethods))
    xl = all_pfmethods

    plt.barh(xt, outdict['overall_recfrac_per_pfmethod'], 0.50)
    plt.yticks(xt, xl)
    plt.xlabel('period-finding method')
    plt.ylabel('overall recovery rate')
    plt.title('overall recovery rate per period-finding method')
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-overall-pfmethod.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 6. bar plot of overall recovery rate per magcol
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    xt = np.arange(len(magcols))
    xl = magcols

    plt.barh(xt, outdict['overall_recfrac_per_magcol'], 0.50)
    plt.yticks(xt, xl)
    plt.xlabel('light curve magnitude column')
    plt.ylabel('overall recovery rate')
    plt.title('overall recovery rate per light curve magcol')
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-overall-magcol.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 7. bar plot of overall recovery rate per aliastype
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    xt = np.arange(len(all_aliastypes))
    xl = all_aliastypes

    plt.barh(xt, outdict['overall_recfrac_per_aliastype'], 0.50)
    plt.yticks(xt, xl)
    plt.xlabel('period recovery status')
    plt.ylabel('overall recovery rate')
    plt.title('overall recovery rate per period recovery status')
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-overall-aliastype.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 8. bar plot of overall recovery rate per vartype
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))

    xt = np.arange(len(all_vartypes))
    xl = all_vartypes

    plt.barh(xt, outdict['overall_recfrac_per_vartype'], 0.50)
    plt.yticks(xt, xl)
    plt.xlabel('periodic variable type')
    plt.ylabel('overall recovery rate')
    plt.title('overall recovery rate per periodic variable type')
    plt.savefig(
        os.path.join(recplotdir,
                     'recfrac-overall-vartype.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # 9. overall recovered period periodogram for objects that aren't actual
    # periodic variables. this effectively should give us the window function of
    # the observations

    notvariable_recovered_periods = np.concatenate([
        precvar['details'][x]['recovery_periods']
        for x in precvar['details'] if
        (precvar['details'][x]['actual_vartype'] is None)
    ])
    notvariable_recovered_lspvals = np.concatenate([
        precvar['details'][x]['recovery_lspvals']
        for x in precvar['details'] if
        (precvar['details'][x]['actual_vartype'] is None)
    ])

    sortind = np.argsort(notvariable_recovered_periods)
    notvariable_recovered_periods = notvariable_recovered_periods[sortind]
    notvariable_recovered_lspvals = notvariable_recovered_lspvals[sortind]

    outdict['notvariable_recovered_periods'] = notvariable_recovered_periods
    outdict['notvariable_recovered_lspvals'] = notvariable_recovered_lspvals

    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))
    plt.plot(notvariable_recovered_periods,
             notvariable_recovered_lspvals,
             ms=1.0,linestyle='none',marker='.')
    plt.xscale('log')
    plt.xlabel('recovered periods [days]')
    plt.ylabel('recovered normalized periodogram power')
    plt.title('periodogram for actual not-variable objects')
    plt.savefig(
        os.path.join(recplotdir,
                     'recovered-periodogram-nonvariables.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')

    # 10. overall recovered period histogram for objects marked
    # not-variable. this gives us the most common periods
    fig = plt.figure(figsize=(6.4*1.5,4.8*1.5))
    plt.hist(notvariable_recovered_periods,bins=np.arange(0.02,300.0,1.0e-3),
             histtype='step')
    plt.xscale('log')
    plt.xlabel('recovered periods [days]')
    plt.ylabel('number of times periods recovered')
    plt.title('recovered period histogram for non-variable objects')
    plt.savefig(
        os.path.join(recplotdir,
                     'recovered-period-hist-nonvariables.%s' % plotfile_ext),
        dpi=100,
        bbox_inches='tight'
    )
    plt.close('all')


    # at the end, write the outdict to a pickle and return it
    outfile = os.path.join(simbasedir, 'periodicvar-recovery-plotresults.pkl')
    with open(outfile,'wb') as outfd:
        pickle.dump(outdict, outfd, pickle.HIGHEST_PROTOCOL)

    return outdict