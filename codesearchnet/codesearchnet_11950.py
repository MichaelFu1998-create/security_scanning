def tic_single_object_crossmatch(ra, dec, radius):
    '''This does a cross-match against the TIC catalog on MAST.

    Speed tests: about 10 crossmatches per second. (-> 3 hours for 10^5 objects
    to crossmatch).

    Parameters
    ----------

    ra,dec : np.array
        The coordinates to cross match against, all in decimal degrees.

    radius : float
        The cross-match radius to use, in decimal degrees.

    Returns
    -------

    dict
        Returns the match results JSON from MAST loaded into a dict.

    '''
    for val in ra,dec,radius:
        if not isinstance(val, float):
            raise AssertionError('plz input ra,dec,radius in decimal degrees')

    # This is a json object
    crossmatchInput = {"fields":[{"name":"ra","type":"float"},
                                 {"name":"dec","type":"float"}],
                       "data":[{"ra":ra,"dec":dec}]}

    request = {"service":"Mast.Tic.Crossmatch",
               "data":crossmatchInput,
               "params":{
                   "raColumn":"ra",
                   "decColumn":"dec",
                   "radius":radius
               },
               "format":"json",
               'removecache':True}

    headers,out_string = _mast_query(request)

    out_data = json.loads(out_string)

    return out_data