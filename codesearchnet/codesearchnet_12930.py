def fill_superseqs(data, samples):
    """
    Fills the superseqs array with seq data from cat.clust
    and fill the edges array with information about paired split locations.
    """

    ## load super to get edges
    io5 = h5py.File(data.clust_database, 'r+')
    superseqs = io5["seqs"]
    splits = io5["splits"]

    ## samples are already sorted
    snames = [i.name for i in samples]
    LOGGER.info("snames %s", snames)

    ## get maxlen again
    maxlen = data._hackersonly["max_fragment_length"] + 20
    LOGGER.info("maxlen inside fill_superseqs is %s", maxlen)

    ## data has to be entered in blocks
    infile = os.path.join(data.dirs.across, data.name+"_catclust.gz")
    clusters = gzip.open(infile, 'r')
    pairdealer = itertools.izip(*[iter(clusters)]*2)

    ## iterate over clusters
    chunks = superseqs.attrs["chunksize"]
    chunksize = chunks[0]
    done = 0
    iloc = 0
    cloc = 0
    chunkseqs = np.zeros(chunks, dtype="|S1")
    chunkedge = np.zeros(chunksize, dtype=np.uint16)

    while 1:
        try:
            done, chunk = clustdealer(pairdealer, 1)
        except IndexError:
            raise IPyradWarningExit("clustfile formatting error in %s", chunk)

        ## if chunk is full put into superseqs and reset counter
        if cloc == chunksize:
            LOGGER.info("cloc chunk writing %s", cloc)
            superseqs[iloc-cloc:iloc] = chunkseqs
            splits[iloc-cloc:iloc] = chunkedge
            ## reset chunkseqs, chunkedge, cloc
            cloc = 0
            chunkseqs = np.zeros((chunksize, len(samples), maxlen), dtype="|S1")
            chunkedge = np.zeros((chunksize), dtype=np.uint16)

        ## get seq and split it
        if chunk:
            try:
                fill = np.zeros((len(samples), maxlen), dtype="|S1")
                fill.fill("N")
                piece = chunk[0].strip().split("\n")
                names = piece[0::2]
                seqs = np.array([list(i) for i in piece[1::2]])
                
                ## fill in the separator if it exists
                separator = np.where(np.all(seqs == 'n', axis=0))[0]
                if np.any(separator):
                    chunkedge[cloc] = separator.min()

                ## fill in the hits
                ## seqs will be (5,) IF the seqs are variable lengths, which 
                ## can happen if it had duplicaes AND there were indels, and 
                ## so the indels did not get aligned
                try:
                    shlen = seqs.shape[1]
                except IndexError as inst:
                    shlen = min([len(x) for x in seqs])

                for name, seq in zip(names, seqs):
                    sidx = snames.index(name.rsplit("_", 1)[0])
                    #fill[sidx, :shlen] = seq[:maxlen]
                    fill[sidx, :shlen] = seq[:shlen]

                ## PUT seqs INTO local ARRAY
                chunkseqs[cloc] = fill

            except Exception as inst:
                LOGGER.info(inst)
                LOGGER.info("\nfill: %s\nshlen %s\nmaxlen %s", fill.shape, shlen, maxlen)
                LOGGER.info("dupe chunk \n{}".format("\n".join(chunk)))

            ## increase counters if there was a chunk
            cloc += 1
            iloc += 1
        if done:
            break

    ## write final leftover chunk
    superseqs[iloc-cloc:,] = chunkseqs[:cloc]
    splits[iloc-cloc:] = chunkedge[:cloc]

    ## close super
    io5.close()
    clusters.close()

    ## edges is filled with splits for paired data.
    LOGGER.info("done filling superseqs")