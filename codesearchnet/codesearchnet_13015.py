def loci2bpp(name, locifile, imap, guidetree,
    minmap=None,
    maxloci=None,
    infer_sptree=0,
    infer_delimit=0,
    delimit_alg=(0, 5),
    seed=12345,
    burnin=1000,
    nsample=10000,
    sampfreq=2,
    thetaprior=(5, 5),
    tauprior=(4, 2, 1),
    traits_df=None,
    nu=0,
    kappa=0,
    useseqdata=1,
    usetraitdata=1,
    cleandata=0,
    wdir=None,
    finetune=(0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01),
    verbose=0):
    """
    Converts loci file format to bpp file format, i.e., concatenated phylip-like
    format, and produces imap and ctl input files for bpp.

    Parameters:
    -----------
    name:
        A prefix name for output files that will be produced
    locifile:
        A .loci file produced by ipyrad.
    imap:
        A Python dictionary with 'species' names as keys, and lists of sample
        names for the values. Any sample that is not included in the imap
        dictionary will be filtered out of the data when converting the .loci
        file into the bpp formatted sequence file. Each species in the imap
        dictionary must also be present in the input 'guidetree'.
    guidetree:
        A newick string species tree hypothesis [e.g., (((a,b),(c,d)),e);]
        All species in the imap dictionary must also be present in the guidetree

    Optional parameters:
    --------------------
    infer_sptree:
        Default=0, only infer parameters on a fixed species tree. If 1, then the
        input tree is treated as a guidetree and tree search is employed to find
        the best tree. The results will include support values for the inferred
        topology.
    infer_delimit:
        Default=0, no delimitation. If 1 then splits in the tree that separate
        'species' will be collapsed to test whether fewer species are a better
        fit to the data than the number in the input guidetree.
    delimit_alg:
        Species delimitation algorithm. This is a tuple. The first value
        is the algorithm (0 or 1) and the following values are arguments
        for the given algorithm. See other ctl files for examples of what the
        delimitation line looks like. This is where you can enter the params
        (e.g., alpha, migration) for the two different algorithms.
        For example, the following args would produce the following ctl lines:
           alg=0, epsilon=5
           > delimit_alg = (0, 5)
           speciesdelimitation = 1 0 5

           alg=1, alpha=2, migration=1
           > delimit_alg = (1, 2, 1)
           speciesdelimitation = 1 1 2 1

           alg=1, alpha=2, migration=1, diagnosis=0, ?=1
           > delimit_alg = (1, 2, 1, 0, 1)
           speciesdelimitation = 1 1 2 1 0 1
    seed:
        A random number seed at start of analysis.
    burnin:
        Number of burnin generations in mcmc
    nsample:
        Number of mcmc generations to run.
    sampfreq:
        How often to sample from the mcmc chain.
    thetaprior:
        Prior on theta (4Neu), gamma distributed. mean = a/b. e.g., (5, 5)
    tauprior
        Prior on root tau, gamma distributed mean = a/b. Last number is 
        dirichlet prior for other taus. e.g., (4, 2, 1)
    traits_df:
        A pandas DataFrame with trait data properly formatted. This means only
        quantitative traits are included, and missing values are NaN.
        The first column contains sample names, with "Indiv" as the header.
        The following columns have a header row with trait names. This script
        will write a CSV trait file with trait values mean-standardized, with
        NaN replaced by "NA", and with sample not present in IMAP removed.
    nu:
        A prior on phenotypic trait variance (0) for iBPP analysis.
    kappa:
        A prior on phenotypic trait mean (0) for iBPP analysis.
    useseqdata:
        If false inference proceeds without sequence data (can be used to test
        the effect of priors on the tree distributions).
    usetraitdata:
        If false inference proceeds without trait data (can be used to test
        the effect of priors on the trait distributions).
    cleandata:
        If 1 then sites with missing or hetero characters are removed.
    wdir:
        A working directory to write files to.
    finetune:
        See bpp documentation.
    verbose:
        If verbose=1 the ctl file text will also be written to screen (stderr).

    """
    ## check args
    if not imap:
        raise IPyradWarningExit(IMAP_REQUIRED)
    if minmap:
        if minmap.keys() != imap.keys():
            raise IPyradWarningExit(KEYS_DIFFER)

    ## working directory, make sure it exists
    if wdir:
        wdir = os.path.abspath(wdir)
        if not os.path.exists(wdir):
            raise IPyradWarningExit(" working directory (wdir) does not exist")
    else:
        wdir = os.path.curdir

    ## if traits_df then we make '.ibpp' files
    prog = 'bpp'
    if isinstance(traits_df, pd.DataFrame):
        prog = 'ibpp'
    outfile = OPJ(wdir, "{}.{}.seq.txt".format(name, prog))
    mapfile = OPJ(wdir, "{}.{}.imap.txt".format(name, prog))

    ## open outhandles
    fout = open(outfile, 'w')
    fmap = open(mapfile, 'w')

    ## parse the loci file
    with open(locifile, 'r') as infile:
        ## split on "//" for legacy compatibility
        loci = infile.read().strip().split("|\n")
        nloci = len(loci)

    ## all samples
    samples = list(itertools.chain(*imap.values()))

    ## iterate over loci, printing to outfile
    nkept = 0
    for iloc in xrange(nloci):
        lines = loci[iloc].split("//")[0].split()
        names = lines[::2]
        names = ["^"+i for i in names]
        seqs = [list(i) for i in lines[1::2]]
        seqlen = len(seqs[0])

        ## whether to skip this locus based on filters below
        skip = 0

        ## if minmap filter for sample coverage
        if minmap:
            covd = {}
            for group, vals in imap.items():
                covd[group] = sum(["^"+i in names for i in vals])
            ## check that coverage is good enough
            if not all([covd[group] >= minmap[group] for group in minmap]):
                skip = 1

        ## too many loci?
        if maxloci:
            if nkept >= maxloci:
                skip = 1

        ## build locus as a string
        if not skip:
            ## convert to phylip with caret starter and replace - with N.
            data = ["{:<30} {}".format(i, "".join(k).replace("-", "N")) for \
                (i, k) in zip(names, seqs) if i[1:] in samples]

            ## if not empty, write to the file
            if data:
                fout.write("{} {}\n\n{}\n\n"\
                           .format(len(data), seqlen, "\n".join(data)))
                nkept += 1

    ## close up shop
    fout.close()

    ## write the imap file:
    data = ["{:<30} {}".format(val, key) for key \
            in sorted(imap) for val in imap[key]]
    fmap.write("\n".join(data))
    fmap.close()

    ## write ctl file
    write_ctl(name, imap, guidetree, nkept,
              infer_sptree, infer_delimit, delimit_alg,
              seed, burnin, nsample, sampfreq,
              thetaprior, tauprior, traits_df, nu, kappa,
              cleandata, useseqdata, usetraitdata, wdir,
              finetune, verbose)

    ## print message?
    sys.stderr.write("new files created ({} loci, {} species, {} samples)\n"\
                     .format(nkept, len(imap.keys()),
                             sum([len(i) for i in imap.values()])))
    sys.stderr.write("  {}.{}.seq.txt\n".format(name, prog))
    sys.stderr.write("  {}.{}.imap.txt\n".format(name, prog))
    sys.stderr.write("  {}.{}.ctl.txt\n".format(name, prog))
    if isinstance(traits_df, pd.DataFrame):
        sys.stderr.write("  {}.{}.traits.txt\n".format(name, prog))

    ## return the ctl file string
    return os.path.abspath(
        "{}.{}.ctl.txt".format(OPJ(wdir, name), prog))