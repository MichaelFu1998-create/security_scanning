def sample_cleanup(data, sample):
    """ stats, cleanup, and link to samples """

    ## get maxlen and depths array from clusters
    maxlens, depths = get_quick_depths(data, sample)

    try:
        depths.max()
    except ValueError:
        ## If depths is an empty array max() will raise
        print("    no clusters found for {}".format(sample.name))
        return

    ## Test if depths is non-empty, but just full of zeros.
    if depths.max():
        ## store which min was used to calculate hidepth here
        sample.stats_dfs.s3["hidepth_min"] = data.paramsdict["mindepth_majrule"]

        ## If our longest sequence is longer than the current max_fragment_length
        ## then update max_fragment_length. For assurance we require that
        ## max len is 4 greater than maxlen, to allow for pair separators.
        hidepths = depths >= data.paramsdict["mindepth_majrule"]
        maxlens = maxlens[hidepths]

        ## Handle the case where there are no hidepth clusters
        if maxlens.any():
            maxlen = int(maxlens.mean() + (2.*maxlens.std()))
        else:
            maxlen = 0
        if maxlen > data._hackersonly["max_fragment_length"]:
            data._hackersonly["max_fragment_length"] = maxlen + 4

        ## make sense of stats
        keepmj = depths[depths >= data.paramsdict["mindepth_majrule"]]
        keepstat = depths[depths >= data.paramsdict["mindepth_statistical"]]

        ## sample summary stat assignments
        sample.stats["state"] = 3
        sample.stats["clusters_total"] = depths.shape[0]
        sample.stats["clusters_hidepth"] = keepmj.shape[0]

        ## store depths histogram as a dict. Limit to first 25 bins
        bars, bins = np.histogram(depths, bins=range(1, 26))
        sample.depths = {int(i):v for i, v in zip(bins, bars) if v}

        ## sample stat assignments
        ## Trap numpy warnings ("mean of empty slice") printed by samples
        ## with few reads.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            sample.stats_dfs.s3["merged_pairs"] = sample.stats.reads_merged
            sample.stats_dfs.s3["clusters_total"] = depths.shape[0]
            try:
                sample.stats_dfs.s3["clusters_hidepth"] = int(sample.stats["clusters_hidepth"])
            except ValueError:
                ## Handle clusters_hidepth == NaN
                sample.stats_dfs.s3["clusters_hidepth"] = 0
            sample.stats_dfs.s3["avg_depth_total"] = depths.mean()
            LOGGER.debug("total depth {}".format(sample.stats_dfs.s3["avg_depth_total"]))
            sample.stats_dfs.s3["avg_depth_mj"] = keepmj.mean()
            LOGGER.debug("mj depth {}".format(sample.stats_dfs.s3["avg_depth_mj"]))
            sample.stats_dfs.s3["avg_depth_stat"] = keepstat.mean()
            sample.stats_dfs.s3["sd_depth_total"] = depths.std()
            sample.stats_dfs.s3["sd_depth_mj"] = keepmj.std()
            sample.stats_dfs.s3["sd_depth_stat"] = keepstat.std()

    else:
        print("    no clusters found for {}".format(sample.name))

    ## Get some stats from the bam files
    ## This is moderately hackish. samtools flagstat returns
    ## the number of reads in the bam file as the first element
    ## of the first line, this call makes this assumption.
    if not data.paramsdict["assembly_method"] == "denovo":
        refmap_stats(data, sample)

    log_level = logging.getLevelName(LOGGER.getEffectiveLevel())

    if not log_level == "DEBUG":
        ## Clean up loose files only if not in DEBUG
        ##- edits/*derep, utemp, *utemp.sort, *htemp, *clust.gz
        derepfile = os.path.join(data.dirs.edits, sample.name+"_derep.fastq")
        mergefile = os.path.join(data.dirs.edits, sample.name+"_merged_.fastq")
        uhandle = os.path.join(data.dirs.clusts, sample.name+".utemp")
        usort = os.path.join(data.dirs.clusts, sample.name+".utemp.sort")
        hhandle = os.path.join(data.dirs.clusts, sample.name+".htemp")
        clusters = os.path.join(data.dirs.clusts, sample.name+".clust.gz")

        for f in [derepfile, mergefile, uhandle, usort, hhandle, clusters]:
            try:
                os.remove(f)
            except:
                pass