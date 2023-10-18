def vcfchunk(data, optim, sidx, chunk, full):
    """
    Function called within make_vcf to run chunks on separate engines.
    """
    ## empty array to be filled before writing
    ## will not actually be optim*maxlen, extra needs to be trimmed
    maxlen = data._hackersonly["max_fragment_length"] + 20

    ## get data sliced (optim chunks at a time)
    hslice = [chunk, chunk+optim]

    ## read all taxa from disk (faster), then subsample taxa with sidx and
    ## keepmask to greatly reduce the memory load
    with h5py.File(data.database, 'r') as co5:
        afilt = co5["filters"][hslice[0]:hslice[1], :]
        keepmask = afilt.sum(axis=1) == 0
        ## apply mask to edges
        aedge = co5["edges"][hslice[0]:hslice[1], :]
        aedge = aedge[keepmask, :]
    del afilt
    ## same memory subsampling.
    with h5py.File(data.clust_database, 'r') as io5:
        ## apply mask to edges to aseqs and acatg
        #aseqs = io5["seqs"][hslice[0]:hslice[1], :, :].view(np.uint8)
        ## need to read in seqs with upper b/c lowercase allele info
        aseqs = np.char.upper(io5["seqs"][hslice[0]:hslice[1], :, :]).view(np.uint8)
        aseqs = aseqs[keepmask, :]
        aseqs = aseqs[:, sidx, :]
        acatg = io5["catgs"][hslice[0]:hslice[1], :, :, :]
        acatg = acatg[keepmask, :]
        acatg = acatg[:, sidx, :, :]
        achrom = io5["chroms"][hslice[0]:hslice[1]]
        achrom = achrom[keepmask, :]        

    LOGGER.info('acatg.shape %s', acatg.shape)
    ## to save memory some columns are stored in diff dtypes until printing
    if not full:
        with h5py.File(data.database, 'r') as co5:
            snps = co5["snps"][hslice[0]:hslice[1], :]
            snps = snps[keepmask, :]
            snps = snps.sum(axis=2)
        snpidxs = snps > 0
        maxsnplen = snps.sum()

    ## vcf info to fill, this is bigger than the actual array
    nrows = maxsnplen
    cols0 = np.zeros(nrows, dtype=np.int64) #h5py.special_dtype(vlen=bytes))
    cols1 = np.zeros(nrows, dtype=np.uint32)
    cols34 = np.zeros((nrows, 2), dtype="S5")
    cols7 = np.zeros((nrows, 1), dtype="S20")

    ## when nsamples is high this blows up memory (e.g., dim=(5M x 500))
    ## so we'll instead create a list of arrays with 10 samples at a time.
    ## maybe later replace this with a h5 array
    tmph = os.path.join(data.dirs.outfiles, ".tmp.{}.h5".format(hslice[0]))
    htmp = h5py.File(tmph, 'w')
    htmp.create_dataset("vcf", shape=(nrows, sum(sidx)), dtype="S24")

    ## which loci passed all filters
    init = 0

    ## write loci that passed after trimming edges, then write snp string
    locindex = np.where(keepmask)[0]
    for iloc in xrange(aseqs.shape[0]):
        edg = aedge[iloc]
        ## grab all seqs between edges
        if not 'pair' in data.paramsdict["datatype"]:
            seq = aseqs[iloc, :, edg[0]:edg[1]+1]
            catg = acatg[iloc, :, edg[0]:edg[1]+1]
            if not full:
                snpidx = snpidxs[iloc, edg[0]:edg[1]+1]
                seq = seq[:, snpidx]
                catg = catg[:, snpidx]
        else:
            seq = np.hstack([aseqs[iloc, :, edg[0]:edg[1]+1],
                             aseqs[iloc, :, edg[2]:edg[3]+1]])
            catg = np.hstack([acatg[iloc, :, edg[0]:edg[1]+1],
                              acatg[iloc, :, edg[2]:edg[3]+1]])
            if not full:
                snpidx = np.hstack([snpidxs[iloc, edg[0]:edg[1]+1],
                                    snpidxs[iloc, edg[2]:edg[3]+1]])
                seq = seq[:, snpidx]
                catg = catg[:, snpidx]

        ## empty arrs to fill
        alleles = np.zeros((nrows, 4), dtype=np.uint8)
        genos = np.zeros((seq.shape[1], sum(sidx)), dtype="S4")
        genos[:] = "./.:"

        ## ----  build string array ----
        pos = 0
        ## If any < 0 this indicates an anonymous locus in denovo+ref assembly
        if achrom[iloc][0] > 0:
            pos = achrom[iloc][1]
            cols0[init:init+seq.shape[1]] = achrom[iloc][0]
            cols1[init:init+seq.shape[1]] = pos + np.where(snpidx)[0] + 1
        else:
            if full:
                cols1[init:init+seq.shape[1]] = pos + np.arange(seq.shape[1]) + 1
            else:
                cols1[init:init+seq.shape[1]] = pos + np.where(snpidx)[0] + 1
                cols0[init:init+seq.shape[1]] = (chunk + locindex[iloc] + 1) * -1

        ## fill reference base
        alleles = reftrick(seq, GETCONS)

        ## get the info string column
        tmp0 = np.sum(catg, axis=2)
        tmp1 = tmp0 != 0
        tmp2 = tmp1.sum(axis=1) > 0
        nsamp = np.sum(tmp1, axis=0)
        depth = np.sum(tmp0, axis=0)
        list7 = [["NS={};DP={}".format(i, j)] for i, j in zip(nsamp, depth)]
        if list7:
            cols7[init:init+seq.shape[1]] = list7

        ## default fill cons sites where no variants
        genos[tmp1.T] = "0/0:"

        ## fill cons genotypes for sites with alt alleles for taxa in order
        mask = alleles[:, 1] == 46
        mask += alleles[:, 1] == 45

        obs = alleles[~mask, :]
        alts = seq[:, ~mask]
        who = np.where(mask == False)[0]
        ## fill variable sites
        for site in xrange(alts.shape[1]):
            bases = alts[:, site]
            #LOGGER.info("bases %s", bases)
            ohere = obs[site][obs[site] != 0]
            #LOGGER.info("ohere %s", ohere)
            alls = np.array([DCONS[i] for i in bases], dtype=np.uint32)
            #LOGGER.info("all %s", alls)
            for jdx in xrange(ohere.shape[0]):
                alls[alls == ohere[jdx]] = jdx

            #LOGGER.info("all2 %s", alls)
            ## fill into array
            for cidx in xrange(catg.shape[0]):
                if tmp2[cidx]:
                    if alls[cidx][0] < 5:
                        genos[who[site], cidx] = "/".join(alls[cidx].astype("S1").tolist())+":"
                    else:
                        genos[who[site], cidx] = "./.:"
                    #LOGGER.info("genos filled: %s %s %s", who[site], cidx, genos)

        ## build geno+depth strings
        ## for each taxon enter 4 catg values
        fulltmp = np.zeros((seq.shape[1], catg.shape[0]), dtype="S24")
        for cidx in xrange(catg.shape[0]):
            ## fill catgs from catgs
            tmp0 = [str(i.sum()) for i in catg[cidx]]
            tmp1 = [",".join(i) for i in catg[cidx].astype("S4").tolist()]
            tmp2 = ["".join(i+j+":"+k) for i, j, k in zip(genos[:, cidx], tmp0, tmp1)]
            ## fill tmp allcidx
            fulltmp[:, cidx] = tmp2
        ## write to h5 for this locus
        htmp["vcf"][init:init+seq.shape[1], :] = fulltmp

        cols34[init:init+seq.shape[1], 0] = alleles[:, 0].view("S1")
        cols34[init:init+seq.shape[1], 1] = [",".join([j for j in i if j]) \
                                    for i in alleles[:, 1:].view("S1").tolist()]

        ## advance counter
        init += seq.shape[1]

    ## trim off empty rows if they exist
    withdat = cols0 != 0
    tot = withdat.sum()

    ## get scaffold names
    faidict = {}
    if (data.paramsdict["assembly_method"] in ["reference", "denovo+reference"]) and \
       (os.path.exists(data.paramsdict["reference_sequence"])):
        fai = pd.read_csv(data.paramsdict["reference_sequence"] + ".fai", 
                names=['scaffold', 'size', 'sumsize', 'a', 'b'],
                sep="\t")
        faidict = {i+1:j for i,j in enumerate(fai.scaffold)}
    try:
        ## This is hax, but it's the only way it will work. The faidict uses positive numbers
        ## for reference sequence mapped loci for the CHROM/POS info, and it uses negative
        ## numbers for anonymous loci. Both are 1 indexed, which is where that last `+ 2` comes from.
        faidict.update({-i:"locus_{}".format(i-1) for i in xrange(chunk+1, chunk + optim + 2)})
        chroms = [faidict[i] for i in cols0]
    except Exception as inst:
        LOGGER.error("Invalid chromosome dictionary indexwat: {}".format(inst))
        LOGGER.debug("faidict {}".format([str(k)+"/"+str(v) for k, v in faidict.items() if "locus" in v]))
        LOGGER.debug("chroms {}".format([x for x in cols0 if x < 0]))
        raise
    cols0 = np.array(chroms)
    #else:
    #    cols0 = np.array(["locus_{}".format(i) for i in cols0-1])

    ## Only write if there is some data that passed filtering
    if tot:
        LOGGER.debug("Writing data to vcf")
        if not full:
            writer = open(data.outfiles.vcf+".{}".format(chunk), 'w')
        else:
            writer = gzip.open(data.outfiles.vcf+".{}".format(chunk), 'w')

        try:
            ## write in iterations b/c it can be freakin huge.
            ## for cols0 and cols1 the 'newaxis' slice and the transpose
            ## are for turning the 1d arrays into column vectors.
            np.savetxt(writer,
                np.concatenate(
                   (cols0[:tot][np.newaxis].T,
                    cols1[:tot][np.newaxis].T,
                    np.array([["."]]*tot, dtype="S1"),
                    cols34[:tot, :],
                    np.array([["13", "PASS"]]*tot, dtype="S4"),
                    cols7[:tot, :],
                    np.array([["GT:DP:CATG"]]*tot, dtype="S10"),
                    htmp["vcf"][:tot, :],
                    ),
                    axis=1),
                delimiter="\t", fmt="%s")
        except Exception as inst:
            LOGGER.error("Error building vcf file - ".format(inst))
            raise
        writer.close()

    ## close and remove tmp h5
    htmp.close()
    os.remove(tmph)