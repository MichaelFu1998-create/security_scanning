def worker_make_arrays(data, sidx, hslice, optim, maxlen):
    """
    Parallelized worker to build array chunks for output files. One main 
    goal here is to keep seqarr to less than ~1GB RAM.
    """
    
    ## big data arrays
    io5 = h5py.File(data.clust_database, 'r')
    co5 = h5py.File(data.database, 'r')
    
    ## temporary storage until writing to h5 array    
    maxsnp = co5["snps"][hslice:hslice+optim].sum()         ## concat later
    maparr = np.zeros((maxsnp, 4), dtype=np.uint32)
    snparr = np.zeros((sum(sidx), maxsnp), dtype="S1")
    bisarr = np.zeros((sum(sidx), maxsnp), dtype="S1")
    seqarr = np.zeros((sum(sidx), maxlen*optim), dtype="S1")

    ## apply all filters and write loci data
    seqleft = 0
    snpleft = 0
    bis = 0                     

    ## edge filter has already been applied to snps, but has not yet been
    ## applied to seqs. The locus filters have not been applied to either yet.
    mapsnp = 0
    totloc = 0

    afilt = co5["filters"][hslice:hslice+optim, :]
    aedge = co5["edges"][hslice:hslice+optim, :]
    asnps = co5["snps"][hslice:hslice+optim, :]
    #aseqs = io5["seqs"][hslice:hslice+optim, sidx, :]
    ## have to run upper on seqs b/c they have lowercase storage of alleles
    aseqs = np.char.upper(io5["seqs"][hslice:hslice+optim, sidx, :])

    ## which loci passed all filters
    keep = np.where(np.sum(afilt, axis=1) == 0)[0]

    ## write loci that passed after trimming edges, then write snp string
    for iloc in keep:
        ## grab r1 seqs between edges
        edg = aedge[iloc]

        ## grab SNPs from seqs already sidx subsampled and edg masked.
        ## needs to be done here before seqs are edgetrimmed.
        getsnps = asnps[iloc].sum(axis=1).astype(np.bool)
        snps = aseqs[iloc, :, getsnps].T

        ## trim edges and split from seqs and concatenate for pairs.
        ## this seq array will be the phy output.
        if not "pair" in data.paramsdict["datatype"]:
            seq = aseqs[iloc, :, edg[0]:edg[1]+1]
        else:
            seq = np.concatenate([aseqs[iloc, :, edg[0]:edg[1]+1],
                                  aseqs[iloc, :, edg[2]:edg[3]+1]], axis=1)

        ## remove cols from seq (phy) array that are all N-
        lcopy = seq
        lcopy[lcopy == "-"] = "N"
        bcols = np.all(lcopy == "N", axis=0)
        seq = seq[:, ~bcols]

        ## put into large array (could put right into h5?)
        seqarr[:, seqleft:seqleft+seq.shape[1]] = seq
        seqleft += seq.shape[1]

        ## subsample all SNPs into an array
        snparr[:, snpleft:snpleft+snps.shape[1]] = snps
        snpleft += snps.shape[1]

        ## Enter each snp into the map file
        for i in xrange(snps.shape[1]):
            ## 1-indexed loci in first column
            ## actual locus number in second column
            ## counter for this locus in third column
            ## snp counter total in fourth column
            maparr[mapsnp, :] = [totloc+1, hslice+iloc, i, mapsnp+1]
            mapsnp += 1

        ## subsample one SNP into an array
        if snps.shape[1]:
            samp = np.random.randint(snps.shape[1])
            bisarr[:, bis] = snps[:, samp]
            bis += 1
            totloc += 1
            
    ## clean up
    io5.close()
    co5.close()
    
    ## trim trailing edges b/c we made the array bigger than needed.
    ridx = np.all(seqarr == "", axis=0)
    seqarr = seqarr[:, ~ridx]
    ridx = np.all(snparr == "", axis=0)
    snparr = snparr[:, ~ridx]
    ridx = np.all(bisarr == "", axis=0)
    bisarr = bisarr[:, ~ridx]
    ridx = np.all(maparr == 0, axis=1)
    maparr = maparr[~ridx, :]

    ## return these three arrays which are pretty small
    ## catg array gets to be pretty huge, so we return only
    return seqarr, snparr, bisarr, maparr