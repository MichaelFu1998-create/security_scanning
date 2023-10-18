def read_and_filter_sqlitecurve(lcfile,
                                columns=None,
                                sqlfilters=None,
                                raiseonfail=False,
                                returnarrays=True,
                                forcerecompress=False,
                                quiet=True):
    '''This reads a HAT sqlitecurve and optionally filters it.

    Parameters
    ----------

    lcfile : str
        The path to the HAT sqlitecurve file.

    columns : list
        A list of columns to extract from the ligh curve file. If None, then
        returns all columns present in the latest `columnlist` in the light
        curve.

    sqlfilters : list of str
        If no None, it must be a list of text SQL filters that apply to the
        columns in the lightcurve.

    raiseonfail : bool
        If this is True, an Exception when reading the LC will crash the
        function instead of failing silently and returning None as the result.

    returnarrays : bool
        If this is True, the output lcdict contains columns as np.arrays instead
        of lists. You generally want this to be True.

    forcerecompress : bool
        If True, the sqlitecurve will be recompressed even if a compressed
        version of it is found. This usually happens when sqlitecurve opening is
        interrupted by the OS for some reason, leaving behind a gzipped and
        un-gzipped copy. By default, this function refuses to overwrite the
        existing gzipped version so if the un-gzipped version is corrupt but
        that one isn't, it can be safely recovered.

    quiet : bool
        If True, will not warn about any problems, even if the light curve
        reading fails (the only clue then will be the return value of
        None). Useful for batch processing of many many light curves.

    Returns
    -------

    tuple : (lcdict, status_message)
        A two-element tuple is returned, with the first element being the
        lcdict.

    '''

    # we're proceeding with reading the LC...
    try:

        # if this file is a gzipped sqlite3 db, then gunzip it
        if '.gz' in lcfile[-4:]:
            lcf = _uncompress_sqlitecurve(lcfile)
        else:
            lcf = lcfile

        db = sql.connect(lcf)
        cur = db.cursor()

        # get the objectinfo from the sqlitecurve
        query = ("select * from objectinfo")
        cur.execute(query)
        objectinfo = cur.fetchone()

        # get the lcinfo from the sqlitecurve
        query = ("select * from lcinfo "
                 "order by version desc limit 1")
        cur.execute(query)
        lcinfo = cur.fetchone()

        (lcversion, lcdatarelease, lccols, lcsortcol,
         lcapertures, lcbestaperture,
         objinfocols, objidcol,
         lcunixtime, lcgitrev, lccomment) = lcinfo

        # load the JSON dicts
        lcapertures = json.loads(lcapertures)
        lcbestaperture = json.loads(lcbestaperture)

        objectinfokeys = objinfocols.split(',')
        objectinfodict = {x:y for (x,y) in zip(objectinfokeys, objectinfo)}
        objectid = objectinfodict[objidcol]

        # need to generate the objectinfo dict and the objectid from the lcinfo
        # columns

        # get the filters from the sqlitecurve
        query = ("select * from filters")
        cur.execute(query)
        filterinfo = cur.fetchall()

        # validate the requested columns
        if columns and all([x in lccols.split(',') for x in columns]):
            LOGINFO('retrieving columns %s' % columns)
            proceed = True
        elif columns is None:
            columns = lccols.split(',')
            proceed = True
        else:
            proceed = False

        # bail out if there's a problem and tell the user what happened
        if not proceed:
            # recompress the lightcurve at the end
            if '.gz' in lcfile[-4:] and lcf:
                _compress_sqlitecurve(lcf, force=forcerecompress)
            LOGERROR('requested columns are invalid!')
            return None, "requested columns are invalid"

        # create the lcdict with the object, lc, and filter info
        lcdict = {'objectid':objectid,
                  'objectinfo':objectinfodict,
                  'objectinfokeys':objectinfokeys,
                  'lcversion':lcversion,
                  'datarelease':lcdatarelease,
                  'columns':columns,
                  'lcsortcol':lcsortcol,
                  'lcapertures':lcapertures,
                  'lcbestaperture':lcbestaperture,
                  'lastupdated':lcunixtime,
                  'lcserver':lcgitrev,
                  'comment':lccomment,
                  'filters':filterinfo}

        # validate the SQL filters for this LC
        if ((sqlfilters is not None) and
            (isinstance(sqlfilters,str) or
             isinstance(sqlfilters, unicode))):

            # give the validator the sqlfilters string and a list of lccols in
            # the lightcurve
            validatedfilters = _validate_sqlitecurve_filters(sqlfilters,
                                                             lccols.split(','))
            if validatedfilters is not None:
                LOGINFO('filtering LC using: %s' % validatedfilters)
                filtersok = True
            else:
                filtersok = False
        else:
            validatedfilters = None
            filtersok = None

        # now read all the required columns in the order indicated

        # we use the validated SQL filter string here
        if validatedfilters is not None:

            query = (
                "select {columns} from lightcurve where {sqlfilter} "
                "order by {sortcol} asc"
            ).format(
                columns=','.join(columns),  # columns is always a list
                sqlfilter=validatedfilters,
                sortcol=lcsortcol
            )
            lcdict['lcfiltersql'] = validatedfilters

        else:
            query = ("select %s from lightcurve order by %s asc") % (
                ','.join(columns),
                lcsortcol
            )

        cur.execute(query)
        lightcurve = cur.fetchall()

        if lightcurve and len(lightcurve) > 0:

            lightcurve = list(zip(*lightcurve))
            lcdict.update({x:y for (x,y) in zip(lcdict['columns'],
                                                lightcurve)})
            lcok = True

            # update the ndet after filtering
            lcdict['objectinfo']['ndet'] = len(lightcurve[0])

        else:
            LOGWARNING('LC for %s has no detections' % lcdict['objectid'])

            # fill the lightcurve with empty lists to indicate that it is empty
            lcdict.update({x:y for (x,y) in
                           zip(lcdict['columns'],
                               [[] for x in lcdict['columns']])})
            lcok = False

        # generate the returned lcdict and status message
        if filtersok is True and lcok:
            statusmsg = 'SQL filters OK, LC OK'
        elif filtersok is None and lcok:
            statusmsg = 'no SQL filters, LC OK'
        elif filtersok is False and lcok:
            statusmsg = 'SQL filters invalid, LC OK'
        else:
            statusmsg = 'LC retrieval failed'

        returnval = (lcdict, statusmsg)

        # recompress the lightcurve at the end
        if '.gz' in lcfile[-4:] and lcf:
            _compress_sqlitecurve(lcf, force=forcerecompress)


        # return ndarrays if that's set
        if returnarrays:
            for column in lcdict['columns']:
                lcdict[column] = np.array([x if x is not None else np.nan
                                           for x in lcdict[column]])

    except Exception as e:

        if not quiet:
            LOGEXCEPTION('could not open sqlitecurve %s' % lcfile)

        returnval = (None, 'error while reading lightcurve file')

        # recompress the lightcurve at the end
        if '.gz' in lcfile[-4:] and lcf:
            _compress_sqlitecurve(lcf, force=forcerecompress)

        if raiseonfail:
            raise

    return returnval