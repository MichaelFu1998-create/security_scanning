def apply_tfa_magseries(lcfile,
                        timecol,
                        magcol,
                        errcol,
                        templateinfo,
                        mintemplatedist_arcmin=10.0,
                        lcformat='hat-sql',
                        lcformatdir=None,
                        interp='nearest',
                        sigclip=5.0):
    '''This applies the TFA correction to an LC given TFA template information.

    Parameters
    ----------

    lcfile : str
        This is the light curve file to apply the TFA correction to.

    timecol,magcol,errcol : str
        These are the column keys in the lcdict for the LC file to apply the TFA
        correction to.

    templateinfo : dict or str
        This is either the dict produced by `tfa_templates_lclist` or the pickle
        produced by the same function.

    mintemplatedist_arcmin : float
        This sets the minimum distance required from the target object for
        objects in the TFA template ensemble. Objects closer than this distance
        will be removed from the ensemble.

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

    interp : str
        This is passed to scipy.interpolate.interp1d as the kind of
        interpolation to use when reforming this light curve to the timebase of
        the TFA templates.

    sigclip : float or sequence of two floats or None
        This is the sigma clip to apply to this light curve before running TFA
        on it.

    Returns
    -------

    str
        This returns the filename of the light curve file generated after TFA
        applications. This is a pickle (that can be read by `lcproc.read_pklc`)
        in the same directory as `lcfile`. The `magcol` will be encoded in the
        filename, so each `magcol` in `lcfile` gets its own output file.

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

    # get the templateinfo from a pickle if necessary
    if isinstance(templateinfo,str) and os.path.exists(templateinfo):
        with open(templateinfo,'rb') as infd:
            templateinfo = pickle.load(infd)

    lcdict = readerfunc(lcfile)
    if ((isinstance(lcdict, (tuple, list))) and
        isinstance(lcdict[0], dict)):
        lcdict = lcdict[0]

    objectid = lcdict['objectid']

    # this is the initial template array
    tmagseries = templateinfo[magcol][
        'template_magseries'
    ][::]

    # if the object itself is in the template ensemble, remove it
    if objectid in templateinfo[magcol]['template_objects']:

        LOGWARNING('object %s found in the TFA template ensemble, removing...' %
                   objectid)

        templateind = templateinfo[magcol]['template_objects'] == objectid

        # get the objects in the tmagseries not corresponding to the current
        # object's index
        tmagseries = tmagseries[~templateind,:]

    # check if there are close matches to the current object in the templates
    object_matches = coordutils.conesearch_kdtree(
        templateinfo[magcol]['template_radecl_kdtree'],
        lcdict['objectinfo']['ra'], lcdict['objectinfo']['decl'],
        mintemplatedist_arcmin/60.0
    )

    if len(object_matches) > 0:

        LOGWARNING(
            "object %s is within %.1f arcminutes of %s "
            "template objects. Will remove these objects "
            "from the template applied to this object." %
            (objectid, mintemplatedist_arcmin, len(object_matches))
        )
        removalind = np.full(
            templateinfo[magcol]['template_objects'].size,
            False, dtype=np.bool
        )
        removalind[np.array(object_matches)] = True
        tmagseries = tmagseries[~removalind,:]

    #
    # finally, proceed to TFA
    #

    # this is the normal matrix
    normal_matrix = np.dot(tmagseries, tmagseries.T)

    # get the inverse of the matrix
    normal_matrix_inverse = spla.pinv2(normal_matrix)

    # get the timebase from the template
    timebase = templateinfo[magcol]['timebase']

    # use this to reform the target lc in the same manner as that for a TFA
    # template LC
    reformed_targetlc = _reform_templatelc_for_tfa((
        lcfile,
        lcformat,
        lcformatdir,
        timecol,
        magcol,
        errcol,
        timebase,
        interp,
        sigclip
    ))

    # calculate the scalar products of the target and template magseries
    scalar_products = np.dot(tmagseries, reformed_targetlc['mags'])

    # calculate the corrections
    corrections = np.dot(normal_matrix_inverse, scalar_products)

    # finally, get the corrected time series for the target object
    corrected_magseries = (
        reformed_targetlc['origmags'] -
        np.dot(tmagseries.T, corrections)
    )

    outdict = {
        'times':timebase,
        'mags':corrected_magseries,
        'errs':reformed_targetlc['errs'],
        'mags_median':np.median(corrected_magseries),
        'mags_mad': np.median(np.abs(corrected_magseries -
                                     np.median(corrected_magseries))),
        'work':{'tmagseries':tmagseries,
                'normal_matrix':normal_matrix,
                'normal_matrix_inverse':normal_matrix_inverse,
                'scalar_products':scalar_products,
                'corrections':corrections,
                'reformed_targetlc':reformed_targetlc},
    }


    # we'll write back the tfa times and mags to the lcdict
    lcdict['tfa'] = outdict
    outfile = os.path.join(
        os.path.dirname(lcfile),
        '%s-tfa-%s-pklc.pkl' % (
            squeeze(objectid).replace(' ','-'),
            magcol
        )
    )
    with open(outfile,'wb') as outfd:
        pickle.dump(lcdict, outfd, pickle.HIGHEST_PROTOCOL)

    return outfile