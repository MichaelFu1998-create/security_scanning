def parallel_concat_lcdir(lcbasedir,
                          objectidlist,
                          aperture='TF1',
                          postfix='.gz',
                          sortby='rjd',
                          normalize=True,
                          outdir=None,
                          recursive=True,
                          nworkers=32,
                          maxworkertasks=1000):
    '''This concatenates all text LCs for the given objectidlist.


    '''

    if not outdir:
        outdir = 'pklcs'

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    tasks = [(lcbasedir, x, {'aperture':aperture,
                             'postfix':postfix,
                             'sortby':sortby,
                             'normalize':normalize,
                             'outdir':outdir,
                             'recursive':recursive}) for x in objectidlist]

    pool = mp.Pool(nworkers, maxtasksperchild=maxworkertasks)
    results = pool.map(parallel_concat_worker, tasks)

    pool.close()
    pool.join()

    return {x:y for (x,y) in zip(objectidlist, results)}