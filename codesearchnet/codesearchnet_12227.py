def parallel_gen_binnedlc_pkls(binnedpkldir,
                               textlcdir,
                               timebinsec,
                               binnedpklglob='*binned*sec*.pkl',
                               textlcglob='*.tfalc.TF1*'):
    '''
    This generates the binnedlc pkls for a directory of such files.

    FIXME: finish this

    '''

    binnedpkls = sorted(glob.glob(os.path.join(binnedpkldir, binnedpklglob)))

    # find all the textlcs associated with these
    textlcs = []

    for bpkl in binnedpkls:

        objectid = HATIDREGEX.findall(bpkl)
        if objectid is not None:
            objectid = objectid[0]

        searchpath = os.path.join(textlcdir, '%s-%s' % (objectid, textlcglob))
        textlcf = glob.glob(searchpath)
        if textlcf:
            textlcs.append(textlcf)
        else:
            textlcs.append(None)