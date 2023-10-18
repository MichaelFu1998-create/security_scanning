def lcdict_to_pickle(lcdict, outfile=None):
    '''This just writes the lcdict to a pickle.

    If outfile is None, then will try to get the name from the
    lcdict['objectid'] and write to <objectid>-hptxtlc.pkl. If that fails, will
    write to a file named hptxtlc.pkl'.

    '''

    if not outfile and lcdict['objectid']:
        outfile = '%s-hplc.pkl' % lcdict['objectid']
    elif not outfile and not lcdict['objectid']:
        outfile = 'hplc.pkl'

    with open(outfile,'wb') as outfd:
        pickle.dump(lcdict, outfd, protocol=pickle.HIGHEST_PROTOCOL)

    if os.path.exists(outfile):
        LOGINFO('lcdict for object: %s -> %s OK' % (lcdict['objectid'],
                                                    outfile))
        return outfile
    else:
        LOGERROR('could not make a pickle for this lcdict!')
        return None