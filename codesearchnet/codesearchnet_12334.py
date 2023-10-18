def _lclist_parallel_worker(task):
    '''This is a parallel worker for makelclist.

    Parameters
    ----------

    task : tuple
        This is a tuple containing the following items:

        task[0] = lcf
        task[1] = columns
        task[2] = lcformat
        task[3] = lcformatdir
        task[4] = lcndetkey

    Returns
    -------

    dict or None
        This contains all of the info for the object processed in this LC read
        operation. If this fails, returns None

    '''

    lcf, columns, lcformat, lcformatdir, lcndetkey = task

    # get the bits needed for lcformat handling
    # NOTE: we re-import things in this worker function because sometimes
    # functions can't be pickled correctly for passing them to worker functions
    # in a processing pool
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

    # we store the full path of the light curve
    lcobjdict = {'lcfname':os.path.abspath(lcf)}

    try:

        # read the light curve in
        lcdict = readerfunc(lcf)

        # this should handle lists/tuples being returned by readerfunc
        # we assume that the first element is the actual lcdict
        # FIXME: figure out how to not need this assumption
        if ( (isinstance(lcdict, (list, tuple))) and
             (isinstance(lcdict[0], dict)) ):
            lcdict = lcdict[0]

        # insert all of the columns
        for colkey in columns:

            if '.' in colkey:
                getkey = colkey.split('.')
            else:
                getkey = [colkey]

            try:
                thiscolval = _dict_get(lcdict, getkey)
            except Exception as e:
                LOGWARNING('column %s does not exist for %s' %
                           (colkey, lcf))
                thiscolval = np.nan

            # update the lcobjdict with this value
            lcobjdict[getkey[-1]] = thiscolval

    except Exception as e:

        LOGEXCEPTION('could not figure out columns for %s' % lcf)

        # insert all of the columns as nans
        for colkey in columns:

            if '.' in colkey:
                getkey = colkey.split('.')
            else:
                getkey = [colkey]

            thiscolval = np.nan

            # update the lclistdict with this value
            lcobjdict[getkey[-1]] = thiscolval

    # now get the actual ndets; this excludes nans and infs
    for dk in lcndetkey:

        try:

            if '.' in dk:
                getdk = dk.split('.')
            else:
                getdk = [dk]

            ndetcol = _dict_get(lcdict, getdk)
            actualndets = ndetcol[np.isfinite(ndetcol)].size
            lcobjdict['%s.ndet' % getdk[-1]] = actualndets

        except Exception as e:
            lcobjdict['%s.ndet' % getdk[-1]] = np.nan


    return lcobjdict