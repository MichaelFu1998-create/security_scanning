def concat_write_pklc(lcbasedir,
                      objectid,
                      aperture='TF1',
                      postfix='.gz',
                      sortby='rjd',
                      normalize=True,
                      outdir=None,
                      recursive=True):
    '''This concatenates all text LCs for the given object and writes to a pklc.

    Basically a rollup for the concatenate_textlcs_for_objectid and
    lcdict_to_pickle functions.

    '''

    concatlcd = concatenate_textlcs_for_objectid(lcbasedir,
                                                 objectid,
                                                 aperture=aperture,
                                                 sortby=sortby,
                                                 normalize=normalize,
                                                 recursive=recursive)

    if not outdir:
        outdir = 'pklcs'

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    outfpath = os.path.join(outdir, '%s-%s-pklc.pkl' % (concatlcd['objectid'],
                                                        aperture))
    pklc = lcdict_to_pickle(concatlcd, outfile=outfpath)
    return pklc