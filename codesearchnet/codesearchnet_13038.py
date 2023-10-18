def muscle_chunker(data, sample):
    """
    Splits the muscle alignment into chunks. Each chunk is run on a separate
    computing core. Because the largest clusters are at the beginning of the 
    clusters file, assigning equal clusters to each file would put all of the 
    large cluster, that take longer to align, near the top. So instead we 
    randomly distribute the clusters among the files. If assembly method is
    reference then this step is just a placeholder and nothing happens. 
    """
    ## log our location for debugging
    LOGGER.info("inside muscle_chunker")

    ## only chunk up denovo data, refdata has its own chunking method which 
    ## makes equal size chunks, instead of uneven chunks like in denovo
    if data.paramsdict["assembly_method"] != "reference":
        ## get the number of clusters
        clustfile = os.path.join(data.dirs.clusts, sample.name+".clust.gz")
        with iter(gzip.open(clustfile, 'rb')) as clustio:
            nloci = sum(1 for i in clustio if "//" in i) // 2
            #tclust = clustio.read().count("//")//2
            optim = (nloci//20) + (nloci%20)
            LOGGER.info("optim for align chunks: %s", optim)

        ## write optim clusters to each tmp file
        clustio = gzip.open(clustfile, 'rb')
        inclusts = iter(clustio.read().strip().split("//\n//\n"))
        
        ## splitting loci so first file is smaller and last file is bigger
        inc = optim // 10
        for idx in range(10):
            ## how big is this chunk?
            this = optim + (idx * inc)
            left = nloci-this
            if idx == 9:
                ## grab everything left
                grabchunk = list(itertools.islice(inclusts, int(1e9)))
            else:
                ## grab next chunks-worth of data
                grabchunk = list(itertools.islice(inclusts, this))
                nloci = left

            ## write the chunk to file
            tmpfile = os.path.join(data.tmpdir, sample.name+"_chunk_{}.ali".format(idx))
            with open(tmpfile, 'wb') as out:
                out.write("//\n//\n".join(grabchunk))

        ## write the chunk to file
        #grabchunk = list(itertools.islice(inclusts, left))
        #if grabchunk:
        #    tmpfile = os.path.join(data.tmpdir, sample.name+"_chunk_9.ali")
        #    with open(tmpfile, 'a') as out:
        #        out.write("\n//\n//\n".join(grabchunk))
        clustio.close()