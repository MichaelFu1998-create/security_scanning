def _starfeatures_worker(task):
    '''
    This wraps starfeatures.

    '''

    try:
        (lcfile, outdir, kdtree, objlist,
         lcflist, neighbor_radius_arcsec,
         deredden, custom_bandpasses, lcformat, lcformatdir) = task

        return get_starfeatures(lcfile, outdir,
                                kdtree, objlist, lcflist,
                                neighbor_radius_arcsec,
                                deredden=deredden,
                                custom_bandpasses=custom_bandpasses,
                                lcformat=lcformat,
                                lcformatdir=lcformatdir)
    except Exception as e:
        return None