def newconsensus(data, sample, tmpchunk, optim):
    """ 
    new faster replacement to consensus 
    """
    ## do reference map funcs?
    isref = "reference" in data.paramsdict["assembly_method"]

    ## temporarily store the mean estimates to Assembly
    data._este = data.stats.error_est.mean()
    data._esth = data.stats.hetero_est.mean()

    ## get number relative to tmp file
    tmpnum = int(tmpchunk.split(".")[-1])

    ## prepare data for reading
    clusters = open(tmpchunk, 'rb')
    pairdealer = itertools.izip(*[iter(clusters)]*2)    
    maxlen = data._hackersonly["max_fragment_length"]

    ## write to tmp cons to file to be combined later
    consenshandle = os.path.join(
        data.dirs.consens, sample.name+"_tmpcons."+str(tmpnum))
    tmp5 = consenshandle.replace("_tmpcons.", "_tmpcats.")
    with h5py.File(tmp5, 'w') as io5:
        io5.create_dataset("cats", (optim, maxlen, 4), dtype=np.uint32)
        io5.create_dataset("alls", (optim, ), dtype=np.uint8)
        io5.create_dataset("chroms", (optim, 3), dtype=np.int64)

        ## local copies to use to fill the arrays
        catarr = io5["cats"][:]
        nallel = io5["alls"][:]
        refarr = io5["chroms"][:]

    ## if reference-mapped then parse the fai to get index number of chroms
    if isref:
        fai = pd.read_csv(data.paramsdict["reference_sequence"] + ".fai", 
                names=['scaffold', 'size', 'sumsize', 'a', 'b'],
                sep="\t")
        faidict = {j:i for i,j in enumerate(fai.scaffold)}

    ## store data for stats counters
    counters = {"name" : tmpnum,
                "heteros": 0,
                "nsites" : 0,
                "nconsens" : 0}

    ## store data for what got filtered
    filters = {"depth" : 0,
               "maxh" : 0,
               "maxn" : 0}

    ## store data for writing
    storeseq = {}

    ## set max limits
    if 'pair' in data.paramsdict["datatype"]:
        maxhet = sum(data.paramsdict["max_Hs_consens"])
        maxn = sum(data.paramsdict["max_Ns_consens"])
    else:
        maxhet = data.paramsdict["max_Hs_consens"][0]
        maxn = data.paramsdict["max_Ns_consens"][0]

    ## load the refmap dictionary if refmapping
    done = 0
    while not done:
        try:
            done, chunk = clustdealer(pairdealer, 1)
        except IndexError:
            raise IPyradError("clustfile formatting error in %s", chunk)

        if chunk:
            ## get names and seqs
            piece = chunk[0].strip().split("\n")
            names = piece[0::2]
            seqs = piece[1::2]

            ## pull replicate read info from seqs
            reps = [int(sname.split(";")[-2][5:]) for sname in names]

            ## IF this is a reference mapped read store the chrom and pos info
            ## -1 defaults to indicating an anonymous locus, since we are using
            ## the faidict as 0 indexed. If chrompos fails it defaults to -1
            ref_position = (-1, 0, 0)
            if isref:
                try:
                    ## parse position from name string
                    name, _, _ = names[0].rsplit(";", 2)
                    chrom, pos0, pos1 = name.rsplit(":", 2)
                    
                    ## pull idx from .fai reference dict 
                    chromint = faidict[chrom] + 1
                    ref_position = (int(chromint), int(pos0), int(pos1))
                    
                except Exception as inst:
                    LOGGER.debug("Reference sequence chrom/pos failed for {}".format(names[0]))
                    LOGGER.debug(inst)
                    
            ## apply read depth filter
            if nfilter1(data, reps):

                ## get stacks of base counts
                sseqs = [list(seq) for seq in seqs]
                arrayed = np.concatenate(
                    [[seq]*rep for seq, rep in zip(sseqs, reps)])
                arrayed = arrayed[:, :maxlen]
                
                ## get consens call for each site, applies paralog-x-site filter
                #consens = np.apply_along_axis(basecall, 0, arrayed, data)
                consens = basecaller(
                    arrayed, 
                    data.paramsdict["mindepth_majrule"], 
                    data.paramsdict["mindepth_statistical"],
                    data._esth, 
                    data._este,
                    )

                ## apply a filter to remove low coverage sites/Ns that
                ## are likely sequence repeat errors. This is only applied to
                ## clusters that already passed the read-depth filter (1)
                if "N" in consens:
                    try:
                        consens, arrayed = removerepeats(consens, arrayed)

                    except ValueError as _:
                        LOGGER.info("Caught a bad chunk w/ all Ns. Skip it.")
                        continue

                ## get hetero sites
                hidx = [i for (i, j) in enumerate(consens) \
                            if j in list("RKSYWM")]
                nheteros = len(hidx)
                
                ## filter for max number of hetero sites
                if nfilter2(nheteros, maxhet):
                    ## filter for maxN, & minlen
                    if nfilter3(consens, maxn):
                        ## counter right now
                        current = counters["nconsens"]
                        ## get N alleles and get lower case in consens
                        consens, nhaps = nfilter4(consens, hidx, arrayed)
                        ## store the number of alleles observed
                        nallel[current] = nhaps

                        ## store a reduced array with only CATG
                        catg = np.array(\
                            [np.sum(arrayed == i, axis=0)  \
                            for i in list("CATG")],
                            dtype='uint32').T
                        catarr[current, :catg.shape[0], :] = catg
                        refarr[current] = ref_position

                        ## store the seqdata for tmpchunk
                        storeseq[counters["name"]] = "".join(list(consens))
                        counters["name"] += 1
                        counters["nconsens"] += 1
                        counters["heteros"] += nheteros
                    else:
                        #LOGGER.debug("@haplo")
                        filters['maxn'] += 1
                else:
                    #LOGGER.debug("@hetero")
                    filters['maxh'] += 1
            else:
                #LOGGER.debug("@depth")
                filters['depth'] += 1
                
    ## close infile io
    clusters.close()

    ## write final consens string chunk
    if storeseq:
        with open(consenshandle, 'wb') as outfile:
            outfile.write("\n".join([">"+sample.name+"_"+str(key)+"\n"+\
                                   str(storeseq[key]) for key in storeseq]))

    ## write to h5 array, this can be a bit slow on big data sets and is not 
    ## currently convered by progressbar movement.
    with h5py.File(tmp5, 'a') as io5:
        io5["cats"][:] = catarr
        io5["alls"][:] = nallel
        io5["chroms"][:] = refarr
    del catarr
    del nallel
    del refarr

    ## return stats
    counters['nsites'] = sum([len(i) for i in storeseq.itervalues()])
    return counters, filters