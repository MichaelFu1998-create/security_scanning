def get_quick_depths(data, sample):
    """ iterate over clustS files to get data """

    ## use existing sample cluster path if it exists, since this
    ## func can be used in step 4 and that can occur after merging
    ## assemblies after step3, and if we then referenced by data.dirs.clusts
    ## the path would be broken.
    ##
    ## If branching at step 3 to test different clust thresholds, the
    ## branched samples will retain the samples.files.clusters of the
    ## parent (which have the clust_threshold value of the parent), so
    ## it will look like nothing has changed. If we call this func
    ## from step 3 then it indicates we are in a branch and should
    ## reset the sample.files.clusters handle to point to the correct
    ## data.dirs.clusts directory. See issue #229.
    ## Easier to just always trust that samples.files.clusters is right,
    ## no matter what step?
    #if sample.files.clusters and not sample.stats.state == 3:
    #    pass
    #else:
    #    ## set cluster file handles
    sample.files.clusters = os.path.join(
         data.dirs.clusts, sample.name+".clustS.gz")

    ## get new clustered loci
    fclust = data.samples[sample.name].files.clusters
    clusters = gzip.open(fclust, 'r')
    pairdealer = itertools.izip(*[iter(clusters)]*2)

    ## storage
    depths = []
    maxlen = []

    ## start with cluster 0
    tdepth = 0
    tlen = 0

    ## iterate until empty
    while 1:
        ## grab next
        try:
            name, seq = pairdealer.next()
        except StopIteration:
            break

        ## if not the end of a cluster
        #print name.strip(), seq.strip()
        if name.strip() == seq.strip():
            depths.append(tdepth)
            maxlen.append(tlen)
            tlen = 0
            tdepth = 0

        else:
            tdepth += int(name.split(";")[-2][5:])
            tlen = len(seq)

    ## return
    clusters.close()
    return np.array(maxlen), np.array(depths)