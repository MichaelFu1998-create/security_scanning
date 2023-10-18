def loci2multinex(name, 
                  locifile, 
                  subsamples=None,
                  outdir=None,
                  maxloci=None,
                  minSNPs=1,
                  seed=12345,
                  mcmc_burnin=int(1e6),
                  mcmc_ngen=int(2e6),
                  mcmc_sample_freq=1000,
                  ):

    """
    Converts loci file format to multiple nexus formatted files, one for 
    each locus, and writes a mrbayes block in the nexus information. The 
    mrbayes block will be set to run 2 replicate chains, for [mcmc_ngen]
    generations, skipping [burnin] steps, and sampling every 
    [mcmc_sample_freq] steps. 


    Parameters:
    -----------
    name: (str)
        A prefix name for output files that will be produced
    locifile: (str)
        A .loci file produced by ipyrad.
    maxloci: (int)
        Limit the number of loci to the first N loci with sufficient sampling
        to be included in the analysis. 
    minSNPs: (int)
        Only include loci that have at least N parsimony informative SNPs.
    seed: (int)
        Random seed used for resolving ambiguities.
    burnin: (int)
        mrbayes nexus block burnin parameter used for 'sump burnin' and 'sumt burnin'.
        The number of generations to skip before starting parameter and tree sampling. 
    mcmc_ngen: (int)
        mrbayes nexus block 'mcmc ngen' and 'mcmc printfreq' parameters. We don't really
        to have any info printed to screen, so these values are set equal. This is the 
        length of the chains that will be run. 
    mcmc_sample_freq: (int)
        mrbayes nexus block 'mcmc samplefreq' parameter. The frequency of sampling from
        the mcmc chain. 

    """

    ## workdir is the top level directory (e.g., analysis-bucky)
    if outdir:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
    else:
        outdir = os.path.curdir

    ## enforce full path names
    outdir = os.path.realpath(outdir)

    ## outdir is a named directory within this (e.g., analysis-bucky/subs/)
    outdir = os.path.join(outdir, "bucky-{}".format(name))
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    else:
        ## remove {number}.nex files in this folder
        ofiles = glob.glob(os.path.join(outdir, "[0-9].nex*"))
        for ofile in ofiles:
            os.remove(ofile)

    ## parse the locifile to a generator
    with open(locifile) as infile:
        loci = (i for i in infile.read().strip().split("|\n"))

    ## convert subsamples to a set
    if not subsamples:
        ## get all sample names from loci
        with open(locifile) as infile:
            subs = set((i.split()[0] for i in infile.readlines() if "//" not in i))
    else:   
        subs = set(subsamples)

    ## keep track of how many loci pass
    lens = len(subs)
    nlocus = 0
    
    ## create subsampled data set
    for loc in loci:
        dat = loc.split("\n")[:-1]

        ## get names and seq from locus
        names = [i.split()[0] for i in dat]
        seqs = np.array([list(i.split()[1]) for i in dat])

        ## check that locus has required samples for each subtree
        if len(set(names).intersection(set(subs))) == lens:
            ## order the same way every time
            seqsamp = seqs[[names.index(tax) for tax in subs]]
            seqsamp = _resolveambig(seqsamp)
            pis = _count_PIS(seqsamp, minSNPs)

            if pis:
                nlocus += 1
                ## remove invariable columns given this subsampling
                copied = seqsamp.copy()
                copied[copied == "-"] = "N"
                rmcol = np.all(copied == "N", axis=0)
                seqsamp = seqsamp[:, ~rmcol]

                ## write to a nexus file
                mdict = dict(zip(subs, [i.tostring() for i in seqsamp]))
                nexmake(mdict, nlocus, outdir, mcmc_burnin, mcmc_ngen, mcmc_sample_freq)

    print "wrote {} nexus files to {}".format(nlocus, outdir)