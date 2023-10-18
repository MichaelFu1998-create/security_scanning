def chunk_clusters(data, sample):
    """ split job into bits and pass to the client """

    ## counter for split job submission
    num = 0

    ## set optim size for chunks in N clusters. The first few chunks take longer
    ## because they contain larger clusters, so we create 4X as many chunks as
    ## processors so that they are split more evenly.
    optim = int((sample.stats.clusters_total // data.cpus) + \
                (sample.stats.clusters_total % data.cpus))

    ## break up the file into smaller tmp files for each engine
    ## chunking by cluster is a bit trickier than chunking by N lines
    chunkslist = []

    ## open to clusters
    with gzip.open(sample.files.clusters, 'rb') as clusters:
        ## create iterator to sample 2 lines at a time
        pairdealer = itertools.izip(*[iter(clusters)]*2)

        ## Use iterator to sample til end of cluster
        done = 0
        while not done:
            ## grab optim clusters and write to file.
            done, chunk = clustdealer(pairdealer, optim)
            chunkhandle = os.path.join(data.dirs.clusts,
                                    "tmp_"+str(sample.name)+"."+str(num*optim))
            if chunk:
                chunkslist.append((optim, chunkhandle))
                with open(chunkhandle, 'wb') as outchunk:
                    outchunk.write("//\n//\n".join(chunk)+"//\n//\n")
                num += 1

    return chunkslist