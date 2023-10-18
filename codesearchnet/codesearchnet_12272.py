def tfa_templates_lclist(
        lclist,
        lcinfo_pkl=None,
        outfile=None,
        target_template_frac=0.1,
        max_target_frac_obs=0.25,
        min_template_number=10,
        max_template_number=1000,
        max_rms=0.15,
        max_mult_above_magmad=1.5,
        max_mult_above_mageta=1.5,
        xieta_bins=20,
        mag_bandpass='sdssr',
        custom_bandpasses=None,
        mag_bright_limit=10.0,
        mag_faint_limit=12.0,
        process_template_lcs=True,
        template_sigclip=5.0,
        template_interpolate='nearest',
        lcformat='hat-sql',
        lcformatdir=None,
        timecols=None,
        magcols=None,
        errcols=None,
        nworkers=NCPUS,
        maxworkertasks=1000,
):
    '''This selects template objects for TFA.

    Selection criteria for TFA template ensemble objects:

    - not variable: use a poly fit to the mag-MAD relation and eta-normal
      variability index to get nonvar objects

    - not more than 10% of the total number of objects in the field or
      `max_tfa_templates` at most

    - allow shuffling of the templates if the target ends up in them

    - nothing with less than the median number of observations in the field

    - sigma-clip the input time series observations

    - TODO: uniform sampling in tangent plane coordinates (we'll need ra and
      decl)

    This also determines the effective cadence that all TFA LCs will be binned
    to as the template LC with the largest number of non-nan observations will
    be used. All template LCs will be renormed to zero.

    Parameters
    ----------

    lclist : list of str
        This is a list of light curves to use as input to generate the template
        set.

    lcinfo_pkl : str or None
        If provided, is a file path to a pickle file created by this function on
        a previous run containing the LC information. This will be loaded
        directly instead of having to re-run LC info collection.

    outfile : str or None
        This is the pickle filename to which the TFA template list will be
        written to. If None, a default file name will be used for this.

    target_template_frac : float
        This is the fraction of total objects in lclist to use for the number of
        templates.

    max_target_frac_obs : float
        This sets the number of templates to generate if the number of
        observations for the light curves is smaller than the number of objects
        in the collection. The number of templates will be set to this fraction
        of the number of observations if this is the case.

    min_template_number : int
        This is the minimum number of templates to generate.

    max_template_number : int
        This is the maximum number of templates to generate. If
        `target_template_frac` times the number of objects is greater than
        `max_template_number`, only `max_template_number` templates will be
        used.

    max_rms : float
        This is the maximum light curve RMS for an object to consider it as a
        possible template ensemble member.

    max_mult_above_magmad : float
        This is the maximum multiplier above the mag-RMS fit to consider an
        object as variable and thus not part of the template ensemble.

    max_mult_above_mageta : float
        This is the maximum multiplier above the mag-eta (variable index) fit to
        consider an object as variable and thus not part of the template
        ensemble.

    mag_bandpass : str
        This sets the key in the light curve dict's objectinfo dict to use as
        the canonical magnitude for the object and apply any magnitude limits
        to.

    custom_bandpasses : dict or None
        This can be used to provide any custom band name keys to the star
        feature collection function.

    mag_bright_limit : float or list of floats
        This sets the brightest mag (in the `mag_bandpass` filter) for a
        potential member of the TFA template ensemble. If this is a single
        float, the value will be used for all magcols. If this is a list of
        floats with len = len(magcols), the specific bright limits will be used
        for each magcol individually.

    mag_faint_limit : float or list of floats
        This sets the faintest mag (in the `mag_bandpass` filter) for a
        potential member of the TFA template ensemble. If this is a single
        float, the value will be used for all magcols. If this is a list of
        floats with len = len(magcols), the specific faint limits will be used
        for each magcol individually.

    process_template_lcs : bool
        If True, will reform the template light curves to the chosen
        time-base. If False, will only select light curves for templates but not
        process them. This is useful for initial exploration of how the template
        LC are selected.

    template_sigclip : float or sequence of floats or None
        This sets the sigma-clip to be applied to the template light curves.

    template_interpolate : str
        This sets the kwarg to pass to `scipy.interpolate.interp1d` to set the
        kind of interpolation to use when reforming light curves to the TFA
        template timebase.

    lcformat : str
        This is the `formatkey` associated with your light curve format, which
        you previously passed in to the `lcproc.register_lcformat`
        function. This will be used to look up how to find and read the light
        curves specified in `basedir` or `use_list_of_filenames`.

    lcformatdir : str or None
        If this is provided, gives the path to a directory when you've stored
        your lcformat description JSONs, other than the usual directories lcproc
        knows to search for them in. Use this along with `lcformat` to specify
        an LC format JSON file that's not currently registered with lcproc.

    timecols : list of str or None
        The timecol keys to use from the lcdict in calculating the features.

    magcols : list of str or None
        The magcol keys to use from the lcdict in calculating the features.

    errcols : list of str or None
        The errcol keys to use from the lcdict in calculating the features.

    nworkers : int
        The number of parallel workers to launch.

    maxworkertasks : int
        The maximum number of tasks to run per worker before it is replaced by a
        fresh one.

    Returns
    -------

    dict
        This function returns a dict that can be passed directly to
        `apply_tfa_magseries` below. It can optionally produce a pickle with the
        same dict, which can also be passed to that function.

    '''

    try:
        formatinfo = get_lcformat(lcformat,
                                  use_lcformat_dir=lcformatdir)
        if formatinfo:
            (dfileglob, readerfunc,
             dtimecols, dmagcols, derrcols,
             magsarefluxes, normfunc) = formatinfo
        else:
            LOGERROR("can't figure out the light curve format")
            return None
    except Exception as e:
        LOGEXCEPTION("can't figure out the light curve format")
        return None

    # override the default timecols, magcols, and errcols
    # using the ones provided to the function
    if timecols is None:
        timecols = dtimecols
    if magcols is None:
        magcols = dmagcols
    if errcols is None:
        errcols = derrcols

    LOGINFO('collecting light curve information for %s objects in list...' %
            len(lclist))

    #
    # check if we have cached results for this run
    #

    # case where we provide a cache info pkl directly
    if lcinfo_pkl and os.path.exists(lcinfo_pkl):

        with open(lcinfo_pkl,'rb') as infd:
            results = pickle.load(infd)

    # case where we don't have an info pickle or an outfile
    elif ((not outfile) and
          os.path.exists('tfa-collected-lcfinfo-%s.pkl' % lcformat)):

        with open('tfa-collected-lcfinfo-%s.pkl' % lcformat, 'rb') as infd:
            results = pickle.load(infd)

    # case where we don't have an info pickle but do have an outfile
    elif (outfile and os.path.exists('tfa-collected-lcfinfo-%s-%s' %
                                     (lcformat, os.path.basename(outfile)))):

        with open(
                'tfa-collected-lcinfo-%s-%s' %
                (lcformat, os.path.basename(outfile)),
                'rb'
        ) as infd:
            results = pickle.load(infd)

    # case where we have to redo the LC info collection
    else:

        # first, we'll collect the light curve info
        tasks = [(x, lcformat, lcformat,
                  timecols, magcols, errcols,
                  custom_bandpasses) for x in lclist]

        pool = mp.Pool(nworkers, maxtasksperchild=maxworkertasks)
        results = pool.map(_collect_tfa_stats, tasks)
        pool.close()
        pool.join()

        # save these results so we don't have to redo if something breaks here
        if not outfile:
            with open('tfa-collected-lcinfo-%s.pkl' % lcformat,'wb') as outfd:
                pickle.dump(results, outfd, pickle.HIGHEST_PROTOCOL)
        else:
            with open(
                    'tfa-collected-lcinfo-%s-%s' %
                    (lcformat, os.path.basename(outfile)),
                    'wb'
            ) as outfd:
                pickle.dump(results, outfd, pickle.HIGHEST_PROTOCOL)

    #
    # now, go through the light curve information
    #

    # find the center RA and center DEC -> median of all LC RAs and DECs
    all_ras = np.array([res['ra'] for res in results])
    all_decls = np.array([res['decl'] for res in results])
    center_ra = np.nanmedian(all_ras)
    center_decl = np.nanmedian(all_decls)

    outdict = {
        'timecols':[],
        'magcols':[],
        'errcols':[],
        'center_ra':center_ra,
        'center_decl':center_decl,
    }

    # for each magcol, we'll generate a separate template list
    for tcol, mcol, ecol in zip(timecols, magcols, errcols):

        if '.' in tcol:
            tcolget = tcol.split('.')
        else:
            tcolget = [tcol]


        # these are the containers for possible template collection LC info
        (lcmag, lcmad, lceta,
         lcndet, lcobj, lcfpaths,
         lcra, lcdecl) = [], [], [], [], [], [], [], []

        outdict['timecols'].append(tcol)
        outdict['magcols'].append(mcol)
        outdict['errcols'].append(ecol)

        # add to the collection of all light curves
        outdict[mcol] = {'collection':{'mag':[],
                                       'mad':[],
                                       'eta':[],
                                       'ndet':[],
                                       'obj':[],
                                       'lcf':[],
                                       'ra':[],
                                       'decl':[]}}

        LOGINFO('magcol: %s, collecting prospective template LC info...' %
                mcol)


        # collect the template LCs for this magcol
        for result in results:

            # we'll only append objects that have all of these elements
            try:

                thismag = result['colorfeat'][mag_bandpass]
                thismad = result[mcol]['mad']
                thiseta = result[mcol]['eta_normal']
                thisndet = result[mcol]['ndet']
                thisobj = result['objectid']
                thislcf = result['lcfpath']
                thisra = result['ra']
                thisdecl = result['decl']

                outdict[mcol]['collection']['mag'].append(thismag)
                outdict[mcol]['collection']['mad'].append(thismad)
                outdict[mcol]['collection']['eta'].append(thiseta)
                outdict[mcol]['collection']['ndet'].append(thisndet)
                outdict[mcol]['collection']['obj'].append(thisobj)
                outdict[mcol]['collection']['lcf'].append(thislcf)
                outdict[mcol]['collection']['ra'].append(thisra)
                outdict[mcol]['collection']['decl'].append(thisdecl)


                # check if we have more than one bright or faint limit elem
                if isinstance(mag_bright_limit, (list, tuple)):
                    use_bright_maglim = mag_bright_limit[
                        magcols.index(mcol)
                    ]
                else:
                    use_bright_maglim = mag_bright_limit
                if isinstance(mag_faint_limit, (list, tuple)):
                    use_faint_maglim = mag_faint_limit[
                        magcols.index(mcol)
                    ]
                else:
                    use_faint_maglim = mag_faint_limit

                # make sure the object lies in the mag limits and RMS limits we
                # set before to try to accept it into the TFA ensemble
                if ((use_bright_maglim < thismag < use_faint_maglim) and
                    (1.4826*thismad < max_rms)):

                    lcmag.append(thismag)
                    lcmad.append(thismad)
                    lceta.append(thiseta)
                    lcndet.append(thisndet)
                    lcobj.append(thisobj)
                    lcfpaths.append(thislcf)
                    lcra.append(thisra)
                    lcdecl.append(thisdecl)

            except Exception as e:
                pass

        # make sure we have enough LCs to work on
        if len(lcobj) >= min_template_number:

            LOGINFO('magcol: %s, %s objects eligible for '
                    'template selection after filtering on mag '
                    'limits (%s, %s) and max RMS (%s)' %
                    (mcol, len(lcobj),
                     mag_bright_limit, mag_faint_limit, max_rms))

            lcmag = np.array(lcmag)
            lcmad = np.array(lcmad)
            lceta = np.array(lceta)
            lcndet = np.array(lcndet)
            lcobj = np.array(lcobj)
            lcfpaths = np.array(lcfpaths)
            lcra = np.array(lcra)
            lcdecl = np.array(lcdecl)

            sortind = np.argsort(lcmag)
            lcmag = lcmag[sortind]
            lcmad = lcmad[sortind]
            lceta = lceta[sortind]
            lcndet = lcndet[sortind]
            lcobj = lcobj[sortind]
            lcfpaths = lcfpaths[sortind]
            lcra = lcra[sortind]
            lcdecl = lcdecl[sortind]

            # 1. get the mag-MAD relation

            # this is needed for spline fitting
            # should take care of the pesky 'x must be strictly increasing' bit
            splfit_ind = np.diff(lcmag) > 0.0
            splfit_ind = np.concatenate((np.array([True]), splfit_ind))

            fit_lcmag = lcmag[splfit_ind]
            fit_lcmad = lcmad[splfit_ind]
            fit_lceta = lceta[splfit_ind]

            magmadfit = np.poly1d(np.polyfit(
                fit_lcmag,
                fit_lcmad,
                2
            ))
            magmadind = lcmad/magmadfit(lcmag) < max_mult_above_magmad

            # 2. get the mag-eta relation
            magetafit = np.poly1d(np.polyfit(
                fit_lcmag,
                fit_lceta,
                2
            ))
            magetaind = magetafit(lcmag)/lceta < max_mult_above_mageta

            # 3. get the median ndet
            median_ndet = np.median(lcndet)
            ndetind = lcndet >= median_ndet

            # form the final template ensemble
            templateind = magmadind & magetaind & ndetind

            # check again if we have enough LCs in the template
            if templateind.sum() >= min_template_number:

                LOGINFO('magcol: %s, %s objects selectable for TFA templates' %
                        (mcol, templateind.sum()))

                templatemag = lcmag[templateind]
                templatemad = lcmad[templateind]
                templateeta = lceta[templateind]
                templatendet = lcndet[templateind]
                templateobj = lcobj[templateind]
                templatelcf = lcfpaths[templateind]
                templatera = lcra[templateind]
                templatedecl = lcdecl[templateind]

                # now, check if we have no more than the required fraction of
                # TFA templates
                target_number_templates = int(target_template_frac*len(results))

                if target_number_templates > max_template_number:
                    target_number_templates = max_template_number

                LOGINFO('magcol: %s, selecting %s TFA templates randomly' %
                        (mcol, target_number_templates))

                # FIXME: how do we select uniformly in xi-eta?
                # 1. 2D histogram the data into binsize (nx, ny)
                # 2. random uniform select from 0 to nx-1, 0 to ny-1
                # 3. pick object from selected bin
                # 4. continue until we have target_number_templates
                # 5. make sure the same object isn't picked twice

                # get the xi-eta
                template_cxi, template_ceta = coordutils.xieta_from_radecl(
                    templatera,
                    templatedecl,
                    center_ra,
                    center_decl
                )

                cxi_bins = np.linspace(template_cxi.min(),
                                       template_cxi.max(),
                                       num=xieta_bins)
                ceta_bins = np.linspace(template_ceta.min(),
                                        template_ceta.max(),
                                        num=xieta_bins)

                digitized_cxi_inds = np.digitize(template_cxi, cxi_bins)
                digitized_ceta_inds = np.digitize(template_ceta, ceta_bins)

                # pick target_number_templates indexes out of the bins
                targetind = npr.choice(xieta_bins,
                                       target_number_templates,
                                       replace=True)

                # put together the template lists
                selected_template_obj = []
                selected_template_lcf = []
                selected_template_ndet = []
                selected_template_ra = []
                selected_template_decl = []
                selected_template_mag = []
                selected_template_mad = []
                selected_template_eta = []

                for ind in targetind:

                    pass


                # select random uniform objects from the template candidates
                targetind = npr.choice(templateobj.size,
                                       target_number_templates,
                                       replace=False)

                templatemag = templatemag[targetind]
                templatemad = templatemad[targetind]
                templateeta = templateeta[targetind]
                templatendet = templatendet[targetind]
                templateobj = templateobj[targetind]
                templatelcf = templatelcf[targetind]
                templatera = templatera[targetind]
                templatedecl = templatedecl[targetind]

                # get the max ndet so far to use that LC as the timebase
                maxndetind = templatendet == templatendet.max()
                timebaselcf = templatelcf[maxndetind][0]
                timebasendet = templatendet[maxndetind][0]

                LOGINFO('magcol: %s, selected %s as template time '
                        'base LC with %s observations' %
                        (mcol, timebaselcf, timebasendet))

                if process_template_lcs:

                    timebaselcdict = readerfunc(timebaselcf)

                    if ( (isinstance(timebaselcdict, (list, tuple))) and
                         (isinstance(timebaselcdict[0], dict)) ):
                        timebaselcdict = timebaselcdict[0]

                    # this is the timebase to use for all of the templates
                    timebase = _dict_get(timebaselcdict, tcolget)

                else:
                    timebase = None

                # also check if the number of templates is longer than the
                # actual timebase of the observations. this will cause issues
                # with overcorrections and will probably break TFA
                if target_number_templates > timebasendet:

                    LOGWARNING('The number of TFA templates (%s) is '
                               'larger than the number of observations '
                               'of the time base (%s). This will likely '
                               'overcorrect all light curves to a '
                               'constant level. '
                               'Will use up to %s x timebase ndet '
                               'templates instead' %
                               (target_number_templates,
                                timebasendet,
                                max_target_frac_obs))

                    # regen the templates based on the new number
                    newmaxtemplates = int(max_target_frac_obs*timebasendet)

                    # choose this number out of the already chosen templates
                    # randomly

                    LOGWARNING('magcol: %s, re-selecting %s TFA '
                               'templates randomly' %
                               (mcol, newmaxtemplates))

                    # FIXME: how do we select uniformly in ra-decl?
                    # 1. 2D histogram the data into binsize (nx, ny)
                    # 2. random uniform select from 0 to nx-1, 0 to ny-1
                    # 3. pick object from selected bin
                    # 4. continue until we have target_number_templates
                    # 5. make sure the same object isn't picked twice

                    # select random uniform objects from the template candidates
                    targetind = npr.choice(templateobj.size,
                                           newmaxtemplates,
                                           replace=False)

                    templatemag = templatemag[targetind]
                    templatemad = templatemad[targetind]
                    templateeta = templateeta[targetind]
                    templatendet = templatendet[targetind]
                    templateobj = templateobj[targetind]
                    templatelcf = templatelcf[targetind]
                    templatera = templatera[targetind]
                    templatedecl = templatedecl[targetind]

                    # get the max ndet so far to use that LC as the timebase
                    maxndetind = templatendet == templatendet.max()
                    timebaselcf = templatelcf[maxndetind][0]
                    timebasendet = templatendet[maxndetind][0]
                    LOGWARNING('magcol: %s, re-selected %s as template time '
                               'base LC with %s observations' %
                               (mcol, timebaselcf, timebasendet))

                    if process_template_lcs:

                        timebaselcdict = readerfunc(timebaselcf)

                        if ( (isinstance(timebaselcdict, (list, tuple))) and
                             (isinstance(timebaselcdict[0], dict)) ):
                            timebaselcdict = timebaselcdict[0]

                        # this is the timebase to use for all of the templates
                        timebase = _dict_get(timebaselcdict, tcolget)

                    else:

                        timebase = None

                #
                # end of check for ntemplates > timebase ndet
                #

                if process_template_lcs:

                    LOGINFO('magcol: %s, reforming TFA template LCs to '
                            ' chosen timebase...' % mcol)

                    # reform all template LCs to this time base, normalize to
                    # zero, and sigclip as requested. this is a parallel op
                    # first, we'll collect the light curve info
                    tasks = [(x, lcformat, lcformatdir,
                              tcol, mcol, ecol,
                              timebase, template_interpolate,
                              template_sigclip) for x
                             in templatelcf]

                    pool = mp.Pool(nworkers, maxtasksperchild=maxworkertasks)
                    reform_results = pool.map(_reform_templatelc_for_tfa, tasks)
                    pool.close()
                    pool.join()

                    # generate a 2D array for the template magseries with
                    # dimensions = (n_objects, n_lcpoints)
                    template_magseries = np.array([x['mags']
                                                   for x in reform_results])
                    template_errseries = np.array([x['errs']
                                                   for x in reform_results])

                else:
                    template_magseries = None
                    template_errseries = None

                # put everything into a templateinfo dict for this magcol
                outdict[mcol].update({
                    'timebaselcf':timebaselcf,
                    'timebase':timebase,
                    'trendfits':{'mag-mad':magmadfit,
                                 'mag-eta':magetafit},
                    'template_objects':templateobj,
                    'template_ra':templatera,
                    'template_decl':templatedecl,
                    'template_mag':templatemag,
                    'template_mad':templatemad,
                    'template_eta':templateeta,
                    'template_ndet':templatendet,
                    'template_magseries':template_magseries,
                    'template_errseries':template_errseries
                })

                # make a KDTree on the template coordinates
                outdict[mcol]['template_radecl_kdtree'] = (
                    coordutils.make_kdtree(
                        templatera, templatedecl
                    )
                )

            # if we don't have enough, return nothing for this magcol
            else:
                LOGERROR('not enough objects meeting requested '
                         'MAD, eta, ndet conditions to '
                         'select templates for magcol: %s' % mcol)
                continue

        else:

            LOGERROR('nobjects: %s, not enough in requested mag range to '
                     'select templates for magcol: %s' % (len(lcobj),mcol))

            continue

        # make the plots for mag-MAD/mag-eta relation and fits used
        plt.plot(lcmag, lcmad, marker='o', linestyle='none', ms=1.0)
        modelmags = np.linspace(lcmag.min(), lcmag.max(), num=1000)
        plt.plot(modelmags, outdict[mcol]['trendfits']['mag-mad'](modelmags))
        plt.yscale('log')
        plt.xlabel('catalog magnitude')
        plt.ylabel('light curve MAD')
        plt.title('catalog mag vs. light curve MAD and fit')
        plt.savefig('catmag-%s-lcmad-fit.png' % mcol,
                    bbox_inches='tight')
        plt.close('all')

        plt.plot(lcmag, lceta, marker='o', linestyle='none', ms=1.0)
        modelmags = np.linspace(lcmag.min(), lcmag.max(), num=1000)
        plt.plot(modelmags, outdict[mcol]['trendfits']['mag-eta'](modelmags))
        plt.yscale('log')
        plt.xlabel('catalog magnitude')
        plt.ylabel('light curve eta variable index')
        plt.title('catalog mag vs. light curve eta and fit')
        plt.savefig('catmag-%s-lceta-fit.png' % mcol,
                    bbox_inches='tight')
        plt.close('all')


    #
    # end of operating on each magcol
    #

    # save the templateinfo dict to a pickle if requested
    if outfile:

        if outfile.endswith('.gz'):
            outfd = gzip.open(outfile,'wb')
        else:
            outfd = open(outfile,'wb')

        with outfd:
            pickle.dump(outdict, outfd, protocol=pickle.HIGHEST_PROTOCOL)

    # return the templateinfo dict
    return outdict