def add_variability_to_fakelc_collection(simbasedir,
                                         override_paramdists=None,
                                         overwrite_existingvar=False):
    '''This adds variability and noise to all fake LCs in `simbasedir`.

    If an object is marked as variable in the `fakelcs-info`.pkl file in
    `simbasedir`, a variable signal will be added to its light curve based on
    its selected type, default period and amplitude distribution, the
    appropriate params, etc. the epochs for each variable object will be chosen
    uniformly from its time-range (and may not necessarily fall on a actual
    observed time). Nonvariable objects will only have noise added as determined
    by their params, but no variable signal will be added.

    Parameters
    ----------

    simbasedir : str
        The directory containing the fake LCs to process.

    override_paramdists : dict
        This can be used to override the stored variable parameters in each fake
        LC. It should be a dict of the following form::

            {'<vartype1>': {'<param1>: a scipy.stats distribution function or
                                       the np.random.randint function,
                            .
                            .
                            .
                            '<paramN>: a scipy.stats distribution function
                                       or the np.random.randint function}

        for any vartype in VARTYPE_LCGEN_MAP. These are used to override the
        default parameter distributions for each variable type.

    overwrite_existingvar : bool
        If this is True, then will overwrite any existing variability in the
        input fake LCs in `simbasedir`.

    Returns
    -------

    dict
        This returns a dict containing the fake LC filenames as keys and
        variability info for each as values.

    '''

    # open the fakelcs-info.pkl
    infof = os.path.join(simbasedir,'fakelcs-info.pkl')
    with open(infof, 'rb') as infd:
        lcinfo = pickle.load(infd)


    lclist = lcinfo['lcfpath']
    varflag = lcinfo['isvariable']
    vartypes = lcinfo['vartype']

    vartind = 0

    varinfo = {}

    # go through all the LCs and add the required type of variability
    for lc, varf, _lcind in zip(lclist, varflag, range(len(lclist))):

        # if this object is variable, add variability
        if varf:

            thisvartype = vartypes[vartind]

            if (override_paramdists and
                isinstance(override_paramdists, dict) and
                thisvartype in override_paramdists and
                isinstance(override_paramdists[thisvartype], dict)):

                thisoverride_paramdists = override_paramdists[thisvartype]
            else:
                thisoverride_paramdists = None


            varlc = add_fakelc_variability(
                lc, thisvartype,
                override_paramdists=thisoverride_paramdists,
                overwrite=overwrite_existingvar
            )
            varinfo[varlc['objectid']] = {'params': varlc['actual_varparams'],
                                          'vartype': varlc['actual_vartype']}

            # update vartind
            vartind = vartind + 1

        else:

            varlc = add_fakelc_variability(
                lc, None,
                overwrite=overwrite_existingvar
            )
            varinfo[varlc['objectid']] = {'params': varlc['actual_varparams'],
                                          'vartype': varlc['actual_vartype']}


    #
    # done with all objects
    #

    # write the varinfo back to the dict and fakelcs-info.pkl
    lcinfo['varinfo'] = varinfo

    tempoutf = '%s.%s' % (infof, md5(npr.bytes(4)).hexdigest()[-8:])
    with open(tempoutf, 'wb') as outfd:
        pickle.dump(lcinfo, outfd, pickle.HIGHEST_PROTOCOL)

    if os.path.exists(tempoutf):
        shutil.copy(tempoutf, infof)
        os.remove(tempoutf)
    else:
        LOGEXCEPTION('could not write output light curve file to dir: %s' %
                     os.path.dirname(tempoutf))
        # fail here
        raise

    return lcinfo