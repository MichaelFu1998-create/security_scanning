def _collect_tfa_stats(task):
    '''
    This is a parallel worker to gather LC stats.

    task[0] = lcfile
    task[1] = lcformat
    task[2] = lcformatdir
    task[3] = timecols
    task[4] = magcols
    task[5] = errcols
    task[6] = custom_bandpasses

    '''

    try:

        (lcfile, lcformat, lcformatdir,
         timecols, magcols, errcols,
         custom_bandpasses) = task

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

        # get the LC into a dict
        lcdict = readerfunc(lcfile)

        # this should handle lists/tuples being returned by readerfunc
        # we assume that the first element is the actual lcdict
        # FIXME: figure out how to not need this assumption
        if ( (isinstance(lcdict, (list, tuple))) and
             (isinstance(lcdict[0], dict)) ):
            lcdict = lcdict[0]

        #
        # collect the necessary stats for this light curve
        #

        # 1. number of observations
        # 2. median mag
        # 3. eta_normal
        # 4. MAD
        # 5. objectid
        # 6. get mags and colors from objectinfo if there's one in lcdict

        if 'objectid' in lcdict:
            objectid = lcdict['objectid']
        elif 'objectinfo' in lcdict and 'objectid' in lcdict['objectinfo']:
            objectid = lcdict['objectinfo']['objectid']
        elif 'objectinfo' in lcdict and 'hatid' in lcdict['objectinfo']:
            objectid = lcdict['objectinfo']['hatid']
        else:
            LOGERROR('no objectid present in lcdict for LC %s, '
                     'using filename prefix as objectid' % lcfile)
            objectid = os.path.splitext(os.path.basename(lcfile))[0]

        if 'objectinfo' in lcdict:

            colorfeat = starfeatures.color_features(
                lcdict['objectinfo'],
                deredden=False,
                custom_bandpasses=custom_bandpasses
            )

        else:
            LOGERROR('no objectinfo dict in lcdict, '
                     'could not get magnitudes for LC %s, '
                     'cannot use for TFA template ensemble' %
                     lcfile)
            return None


        # this is the initial dict
        resultdict = {'objectid':objectid,
                      'ra':lcdict['objectinfo']['ra'],
                      'decl':lcdict['objectinfo']['decl'],
                      'colorfeat':colorfeat,
                      'lcfpath':os.path.abspath(lcfile),
                      'lcformat':lcformat,
                      'lcformatdir':lcformatdir,
                      'timecols':timecols,
                      'magcols':magcols,
                      'errcols':errcols}

        for tcol, mcol, ecol in zip(timecols, magcols, errcols):

            try:

                # dereference the columns and get them from the lcdict
                if '.' in tcol:
                    tcolget = tcol.split('.')
                else:
                    tcolget = [tcol]
                times = _dict_get(lcdict, tcolget)

                if '.' in mcol:
                    mcolget = mcol.split('.')
                else:
                    mcolget = [mcol]
                mags = _dict_get(lcdict, mcolget)

                if '.' in ecol:
                    ecolget = ecol.split('.')
                else:
                    ecolget = [ecol]
                errs = _dict_get(lcdict, ecolget)

                # normalize here if not using special normalization
                if normfunc is None:
                    ntimes, nmags = normalize_magseries(
                        times, mags,
                        magsarefluxes=magsarefluxes
                    )

                    times, mags, errs = ntimes, nmags, errs

                # get the variability features for this object
                varfeat = varfeatures.all_nonperiodic_features(
                    times, mags, errs
                )

                resultdict[mcol] = varfeat

            except Exception as e:

                LOGEXCEPTION('%s, magcol: %s, probably ran into all-nans' %
                             (lcfile, mcol))
                resultdict[mcol] = {'ndet':0,
                                    'mad':np.nan,
                                    'eta_normal':np.nan}


        return resultdict

    except Exception as e:

        LOGEXCEPTION('could not execute get_tfa_stats for task: %s' %
                     repr(task))
        return None