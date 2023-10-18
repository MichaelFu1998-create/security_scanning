def sub_build_clustbits(data, usort, nseeds):
    """
    A subfunction of build_clustbits to allow progress tracking. This func
    splits the unaligned clusters into bits for aligning on separate cores.
    """

    ## load FULL concat fasta file into a dict. This could cause RAM issues.
    ## this file has iupac codes in it, not ambigs resolved, and is gzipped.
    LOGGER.info("loading full _catcons file into memory")
    allcons = {}
    conshandle = os.path.join(data.dirs.across, data.name+"_catcons.tmp")
    with gzip.open(conshandle, 'rb') as iocons:
        cons = itertools.izip(*[iter(iocons)]*2)
        for namestr, seq in cons:
            nnn, sss = [i.strip() for i in namestr, seq]
            allcons[nnn[1:]] = sss

    ## set optim to approximately 4 chunks per core. Smaller allows for a bit
    ## cleaner looking progress bar. 40 cores will make 160 files.
    optim = ((nseeds // (data.cpus*4)) + (nseeds % (data.cpus*4)))
    LOGGER.info("building clustbits, optim=%s, nseeds=%s, cpus=%s",
                optim, nseeds, data.cpus)

    ## iterate through usort grabbing seeds and matches
    with open(usort, 'rb') as insort:
        ## iterator, seed null, and seqlist null
        isort = iter(insort)
        loci = 0
        lastseed = 0
        fseqs = []
        seqlist = []
        seqsize = 0

        while 1:
            ## grab the next line
            try:
                hit, seed, ori = isort.next().strip().split()
            except StopIteration:
                break

            try:
                ## if same seed, append match
                if seed != lastseed:
                    ## store the last fseq, count it, and clear it
                    if fseqs:
                        seqlist.append("\n".join(fseqs))
                        seqsize += 1
                        fseqs = []
                    ## occasionally write to file
                    if seqsize >= optim:
                        if seqlist:
                            loci += seqsize
                            with open(os.path.join(data.tmpdir,
                                data.name+".chunk_{}".format(loci)), 'w') as clustsout:
                                LOGGER.debug("writing chunk - seqsize {} loci {} {}".format(seqsize, loci, clustsout.name))
                                clustsout.write("\n//\n//\n".join(seqlist)+"\n//\n//\n")
                            ## reset list and counter
                            seqlist = []
                            seqsize = 0
    
                    ## store the new seed on top of fseq
                    fseqs.append(">{}\n{}".format(seed, allcons[seed]))
                    lastseed = seed
    
                ## add match to the seed
                seq = allcons[hit]
                ## revcomp if orientation is reversed
                if ori == "-":
                    seq = fullcomp(seq)[::-1]
                fseqs.append(">{}\n{}".format(hit, seq))
            except KeyError as inst:
                ## Caught bad seed or hit? Log and continue.
                LOGGER.error("Bad Seed/Hit: seqsize {}\tloci {}\tseed {}\thit {}".format(seqsize, loci, seed, hit))

    ## write whatever is left over to the clusts file
    if fseqs:
        seqlist.append("\n".join(fseqs))
        seqsize += 1
        loci += seqsize
    if seqlist:
        with open(os.path.join(data.tmpdir,
            data.name+".chunk_{}".format(loci)), 'w') as clustsout:
            clustsout.write("\n//\n//\n".join(seqlist)+"\n//\n//\n")

    ## final progress and cleanup
    del allcons
    clustbits = glob.glob(os.path.join(data.tmpdir, data.name+".chunk_*"))

    ## return stuff
    return clustbits, loci