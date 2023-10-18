def make_stats(data, samples, samplecounts, locuscounts):
    """ write the output stats file and save to Assembly obj."""

    ## get meta info
    with h5py.File(data.clust_database, 'r') as io5:
        anames = io5["seqs"].attrs["samples"]
        nloci = io5["seqs"].shape[0]
        optim = io5["seqs"].attrs["chunksize"][0]

    ## open the out handle. This will have three data frames saved to it.
    ## locus_filtering, sample_coverages, and snp_distributions
    data.stats_files.s7 = os.path.join(data.dirs.outfiles,
                                       data.name+"_stats.txt")
    outstats = io.open(data.stats_files.s7, 'w', encoding="utf-8")

    ########################################################################
    ## get stats for locus_filtering, use chunking.
    filters = np.zeros(6, dtype=int)
    passed = 0
    start = 0

    piscounts = Counter()
    varcounts = Counter()
    for i in range(200):
        piscounts[i] = 0
        varcounts[i] = 0


    applied = pd.Series([0]*8,
        name="applied_order",
        index=[
        "total_prefiltered_loci",
        "filtered_by_rm_duplicates",
        "filtered_by_max_indels",
        "filtered_by_max_snps",
        "filtered_by_max_shared_het",
        "filtered_by_min_sample",
        "filtered_by_max_alleles",
        "total_filtered_loci"])

    ## load the h5 database
    co5 = h5py.File(data.database, 'r')

    while start < nloci:
        hslice = [start, start+optim]
        ## load each array
        afilt = co5["filters"][hslice[0]:hslice[1], ]
        asnps = co5["snps"][hslice[0]:hslice[1], ]

        ## get subarray results from filter array
        # max_indels, max_snps, max_hets, min_samps, bad_edges, max_alleles
        filters += afilt.sum(axis=0)
        applied["filtered_by_rm_duplicates"] += afilt[:, 0].sum()
        mask = afilt[:, 0].astype(np.bool)
        applied["filtered_by_max_indels"] += afilt[~mask, 1].sum()
        mask = afilt[:, 0:2].sum(axis=1).astype(np.bool)
        applied["filtered_by_max_snps"] += afilt[~mask, 2].sum()
        mask = afilt[:, 0:3].sum(axis=1).astype(np.bool)
        applied["filtered_by_max_shared_het"] += afilt[~mask, 3].sum()
        mask = afilt[:, 0:4].sum(axis=1).astype(np.bool)
        applied["filtered_by_min_sample"] += afilt[~mask, 4].sum()
        mask = afilt[:, 0:5].sum(axis=1).astype(np.bool)
        applied["filtered_by_max_alleles"] += afilt[~mask, 5].sum()

        passed += np.sum(afilt.sum(axis=1) == 0)

        ## get filter to count snps for only passed loci
        ## should we filter by all vars, or just by pis? doing all var now.
        apply_filter = afilt.sum(axis=1).astype(np.bool)

        ## get snps counts
        snplocs = asnps[~apply_filter, :].sum(axis=1)
        varlocs = snplocs.sum(axis=1)
        varcounts.update(Counter(varlocs))
        #snpcounts.update(Counter(snplocs[:, 0]))
        piscounts.update(Counter(snplocs[:, 1]))

        ## increase counter to advance through h5 database
        start += optim

    ## record filtering of loci from total to final
    filtdat = pd.Series(np.concatenate([[nloci], filters, [passed]]),
        name="total_filters",
        index=[
        "total_prefiltered_loci",
        "filtered_by_rm_duplicates",
        "filtered_by_max_indels",
        "filtered_by_max_snps",
        "filtered_by_max_shared_het",
        "filtered_by_min_sample",
        "filtered_by_max_alleles",
        "total_filtered_loci"])


    retained = pd.Series([0]*8,
        name="retained_loci",
        index=[
        "total_prefiltered_loci",
        "filtered_by_rm_duplicates",
        "filtered_by_max_indels",
        "filtered_by_max_snps",
        "filtered_by_max_shared_het",
        "filtered_by_min_sample",
        "filtered_by_max_alleles",
        "total_filtered_loci"])
    retained["total_prefiltered_loci"] = nloci
    retained["filtered_by_rm_duplicates"] = nloci - applied["filtered_by_rm_duplicates"]
    retained["filtered_by_max_indels"] = retained["filtered_by_rm_duplicates"] - applied["filtered_by_max_indels"]
    retained["filtered_by_max_snps"] = retained["filtered_by_max_indels"] - applied["filtered_by_max_snps"]
    retained["filtered_by_max_shared_het"] = retained["filtered_by_max_snps"] - applied["filtered_by_max_shared_het"]
    retained["filtered_by_min_sample"] = retained["filtered_by_max_shared_het"] - applied["filtered_by_min_sample"]
    retained["filtered_by_max_alleles"] = retained["filtered_by_min_sample"] - applied["filtered_by_max_alleles"]
    retained["total_filtered_loci"] = passed


    print(u"\n\n## The number of loci caught by each filter."+\
          u"\n## ipyrad API location: [assembly].stats_dfs.s7_filters\n",
          file=outstats)
    data.stats_dfs.s7_filters = pd.DataFrame([filtdat, applied, retained]).T
    data.stats_dfs.s7_filters.to_string(buf=outstats)


    ########################################################################
    ## make dataframe of sample_coverages
    ## samplecounts is len of anames from db. Save only samples in samples.
    #print(samplecounts)
    #samples = [i.name for i in samples]
    ## get sample names in the order of anames
    #sids = [list(anames).index(i) for i in samples]
    #covdict = {name: val for name, val in zip(np.array(samples)[sidx], samplecounts)}
    #covdict = {name: val for name, val in zip(samples, samplecounts[sidx])}
    covdict = pd.Series(samplecounts, name="sample_coverage", index=anames)
    covdict = covdict[covdict != 0]
    print(u"\n\n\n## The number of loci recovered for each Sample."+\
          u"\n## ipyrad API location: [assembly].stats_dfs.s7_samples\n",
          file=outstats)
    data.stats_dfs.s7_samples = pd.DataFrame(covdict)
    data.stats_dfs.s7_samples.to_string(buf=outstats)


    ########################################################################
    ## get stats for locus coverage
    lrange = range(1, len(samples)+1)
    locdat = pd.Series(locuscounts, name="locus_coverage", index=lrange)
    start = data.paramsdict["min_samples_locus"]-1
    locsums = pd.Series({i: np.sum(locdat.values[start:i]) for i in lrange},
                        name="sum_coverage", index=lrange)
    print(u"\n\n\n## The number of loci for which N taxa have data."+\
          u"\n## ipyrad API location: [assembly].stats_dfs.s7_loci\n",
          file=outstats)
    data.stats_dfs.s7_loci = pd.concat([locdat, locsums], axis=1)
    data.stats_dfs.s7_loci.to_string(buf=outstats)


    #########################################################################
    ## get stats for SNP_distribution
    try:
        smax = max([i+1 for i in varcounts if varcounts[i]])
    except Exception as inst:
        raise IPyradWarningExit("""
    Exception: empty varcounts array. This could be because no samples 
    passed filtering, or it could be because you have overzealous filtering.
    Check the values for `trim_loci` and make sure you are not trimming the
    edge too far
    """)

    vardat = pd.Series(varcounts, name="var", index=range(smax)).fillna(0)
    sumd = {}
    for i in range(smax):
        sumd[i] = np.sum([i*vardat.values[i] for i in range(i+1)])
    varsums = pd.Series(sumd, name="sum_var", index=range(smax))

    pisdat = pd.Series(piscounts, name="pis", index=range(smax)).fillna(0)
    sumd = {}
    for i in range(smax):
        sumd[i] = np.sum([i*pisdat.values[i] for i in range(i+1)])
    pissums = pd.Series(sumd, name="sum_pis", index=range(smax))

    print(u"\n\n\n## The distribution of SNPs (var and pis) per locus."+\
          u"\n## var = Number of loci with n variable sites (pis + autapomorphies)"+\
          u"\n## pis = Number of loci with n parsimony informative site (minor allele in >1 sample)"+\
          u"\n## ipyrad API location: [assembly].stats_dfs.s7_snps\n",
          file=outstats)
    data.stats_dfs.s7_snps = pd.concat([vardat, varsums, pisdat, pissums],
                                        axis=1)
    data.stats_dfs.s7_snps.to_string(buf=outstats)

    ##########################################################################
    ## print the stats summary (-r summary) with final sample loci data.
    fullstat = data.stats
    fullstat['state'] = 7
    fullstat["loci_in_assembly"] = data.stats_dfs.s7_samples

    print(u"\n\n\n## Final Sample stats summary\n", file=outstats)
    fullstat.to_string(buf=outstats)

    ## close it
    outstats.close()
    co5.close()