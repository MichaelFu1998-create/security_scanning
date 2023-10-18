def make_outfiles(data, samples, output_formats, ipyclient):
    """
    Get desired formats from paramsdict and write files to outfiles
    directory.
    """

    ## will iterate optim loci at a time
    with h5py.File(data.clust_database, 'r') as io5:
        optim = io5["seqs"].attrs["chunksize"][0]
        nloci = io5["seqs"].shape[0]

        ## get name and snp padding
        anames = io5["seqs"].attrs["samples"]
        snames = [i.name for i in samples]
        ## get only snames in this data set sorted in the order they are in io5
        names = [i for i in anames if i in snames]
        pnames, _ = padnames(names)


    ## get names boolean
    sidx = np.array([i in snames for i in anames])
    assert len(pnames) == sum(sidx)

    ## get names index in order of pnames
    #sindx = [list(anames).index(i) for i in snames]

    ## send off outputs as parallel jobs
    lbview = ipyclient.load_balanced_view()
    start = time.time()
    results = {}

    ## build arrays and outputs from arrays.
    ## these arrays are keys in the tmp h5 array: seqarr, snparr, bisarr, maparr
    boss_make_arrays(data, sidx, optim, nloci, ipyclient)

    start = time.time()
    ## phy and partitions are a default output ({}.phy, {}.phy.partitions)
    if "p" in output_formats:
        data.outfiles.phy = os.path.join(data.dirs.outfiles, data.name+".phy")
        async = lbview.apply(write_phy, *[data, sidx, pnames])
        results['phy'] = async

    ## nexus format includes ... additional information ({}.nex)
    if "n" in output_formats:
        data.outfiles.nexus = os.path.join(data.dirs.outfiles, data.name+".nex")
        async = lbview.apply(write_nex, *[data, sidx, pnames])
        results['nexus'] = async

    ## snps is actually all snps written in phylip format ({}.snps.phy)
    if "s" in output_formats:
        data.outfiles.snpsmap = os.path.join(data.dirs.outfiles, data.name+".snps.map")
        data.outfiles.snpsphy = os.path.join(data.dirs.outfiles, data.name+".snps.phy")
        async = lbview.apply(write_snps, *[data, sidx, pnames])
        results['snps'] = async
        async = lbview.apply(write_snps_map, data)
        results['snpsmap'] = async

    ## usnps is one randomly sampled snp from each locus ({}.u.snps.phy)
    if "u" in output_formats:
        data.outfiles.usnpsphy = os.path.join(data.dirs.outfiles, data.name+".u.snps.phy")
        async = lbview.apply(write_usnps, *[data, sidx, pnames])
        results['usnps'] = async

    ## str and ustr are for structure analyses. A fairly outdated format, six
    ## columns of empty space. Full and subsample included ({}.str, {}.u.str)
    if "k" in output_formats:
        data.outfiles.str = os.path.join(data.dirs.outfiles, data.name+".str")
        data.outfiles.ustr = os.path.join(data.dirs.outfiles, data.name+".ustr")        
        async = lbview.apply(write_str, *[data, sidx, pnames])
        results['structure'] = async

    ## geno output is for admixture and other software. We include all SNPs,
    ## but also a .map file which has "distances" between SNPs.
    if 'g' in output_formats:
        data.outfiles.geno = os.path.join(data.dirs.outfiles, data.name+".geno")
        data.outfiles.ugeno = os.path.join(data.dirs.outfiles, data.name+".u.geno")
        async = lbview.apply(write_geno, *[data, sidx])
        results['geno'] = async

    ## G-PhoCS output. Have to use cap G here cuz little g is already taken, lol.
    if 'G' in output_formats:
        data.outfiles.gphocs = os.path.join(data.dirs.outfiles, data.name+".gphocs")
        async = lbview.apply(write_gphocs, *[data, sidx])
        results['gphocs'] = async

    ## wait for finished outfiles
    while 1:
        readies = [i.ready() for i in results.values()]
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(len(readies), sum(readies),
            " writing outfiles      | {} | s7 |".format(elapsed), 
            spacer=data._spacer)
        time.sleep(0.1)
        if all(readies):
            break
    print("")

    ## check for errors
    for suff, async in results.items():
        if not async.successful():
            print("  Warning: error encountered while writing {} outfile: {}"\
                  .format(suff, async.exception()))
            LOGGER.error("  Warning: error in writing %s outfile: %s", \
                         suff, async.exception())

    ## remove the tmparrays
    tmparrs = os.path.join(data.dirs.outfiles, "tmp-{}.h5".format(data.name))
    os.remove(tmparrs)