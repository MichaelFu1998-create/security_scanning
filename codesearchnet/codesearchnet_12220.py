def concatenate_textlcs_for_objectid(lcbasedir,
                                     objectid,
                                     aperture='TF1',
                                     postfix='.gz',
                                     sortby='rjd',
                                     normalize=True,
                                     recursive=True):
    '''This concatenates all text LCs for an objectid with the given aperture.

    Does not care about overlaps or duplicates. The light curves must all be
    from the same aperture.

    The intended use is to concatenate light curves across CCDs or instrument
    changes for a single object. These can then be normalized later using
    standard astrobase tools to search for variablity and/or periodicity.


    lcbasedir is the directory to start searching in.

    objectid is the object to search for.

    aperture is the aperture postfix to use: (TF1 = aperture 1,
                                              TF2 = aperture 2,
                                              TF3 = aperture 3)

    sortby is a column to sort the final concatenated light curve by in
    ascending order.

    If normalize is True, then each light curve's magnitude columns are
    normalized to zero, and the whole light curve is then normalized to the
    global median magnitude for each magnitude column.

    If recursive is True, then the function will search recursively in lcbasedir
    for any light curves matching the specified criteria. This may take a while,
    especially on network filesystems.

    The returned lcdict has an extra column: 'lcn' that tracks which measurement
    belongs to which input light curve. This can be used with
    lcdict['concatenated'] which relates input light curve index to input light
    curve filepath. Finally, there is an 'nconcatenated' key in the lcdict that
    contains the total number of concatenated light curves.

    '''
    LOGINFO('looking for light curves for %s, aperture %s in directory: %s'
            % (objectid, aperture, lcbasedir))

    if recursive is False:

        matching = glob.glob(os.path.join(lcbasedir,
                                          '*%s*%s*%s' % (objectid,
                                                         aperture,
                                                         postfix)))
    else:
        # use recursive glob for Python 3.5+
        if sys.version_info[:2] > (3,4):

            matching = glob.glob(os.path.join(lcbasedir,
                                              '**',
                                              '*%s*%s*%s' % (objectid,
                                                             aperture,
                                                             postfix)),
                                 recursive=True)
            LOGINFO('found %s files: %s' % (len(matching), repr(matching)))

        # otherwise, use os.walk and glob
        else:

            # use os.walk to go through the directories
            walker = os.walk(lcbasedir)
            matching = []

            for root, dirs, _files in walker:
                for sdir in dirs:
                    searchpath = os.path.join(root,
                                              sdir,
                                              '*%s*%s*%s' % (objectid,
                                                             aperture,
                                                             postfix))
                    foundfiles = glob.glob(searchpath)

                    if foundfiles:
                        matching.extend(foundfiles)
                        LOGINFO(
                            'found %s in dir: %s' % (repr(foundfiles),
                                                     os.path.join(root,sdir))
                        )

    # now that we have all the files, concatenate them
    # a single file will be returned as normalized
    if matching and len(matching) > 0:
        clcdict = concatenate_textlcs(matching,
                                      sortby=sortby,
                                      normalize=normalize)
        return clcdict
    else:
        LOGERROR('did not find any light curves for %s and aperture %s' %
                 (objectid, aperture))
        return None