def parallel_varfeatures(lclist,
                         outdir,
                         maxobjects=None,
                         timecols=None,
                         magcols=None,
                         errcols=None,
                         mindet=1000,
                         lcformat='hat-sql',
                         lcformatdir=None,
                         nworkers=NCPUS):
    '''This runs variable feature extraction in parallel for all LCs in `lclist`.

    Parameters
    ----------

    lclist : list of str
        The list of light curve file names to process.

    outdir : str
        The directory where the output varfeatures pickle files will be written.

    maxobjects : int
        The number of LCs to process from `lclist`.

    timecols : list of str or None
        The timecol keys to use from the lcdict in calculating the features.

    magcols : list of str or None
        The magcol keys to use from the lcdict in calculating the features.

    errcols : list of str or None
        The errcol keys to use from the lcdict in calculating the features.

    mindet : int
        The minimum number of LC points required to generate variability
        features.

    lcformat : str
        This is the `formatkey` associated with your light curve format, which
        you previously passed in to the `lcproc.register_lcformat`
        function. This will be used to look up how to find and read the light
        curves specified in `basedir` or `use_list_of_filenames`.

    lcformatdir : str or None
        If this is provided, gives the path to a directory when you've stored
        your lcformat description JSONs, other than the usual directories lcproc
        knows to search for them in. Use this along with `lcformat` to specify
        an LC format JSON file that's not currently registered with lcproc.

    nworkers : int
        The number of parallel workers to launch.

    Returns
    -------

    dict
        A dict with key:val pairs of input LC file name : the generated
        variability features pickles for each of the input LCs, with results for
        each magcol in the input `magcol` or light curve format's default
        `magcol` list.

    '''
    # make sure to make the output directory if it doesn't exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if maxobjects:
        lclist = lclist[:maxobjects]

    tasks = [(x, outdir, timecols, magcols, errcols, mindet,
              lcformat, lcformatdir) for x in lclist]

    with ProcessPoolExecutor(max_workers=nworkers) as executor:
        resultfutures = executor.map(varfeatures_worker, tasks)

    results = [x for x in resultfutures]
    resdict = {os.path.basename(x):y for (x,y) in zip(lclist, results)}

    return resdict