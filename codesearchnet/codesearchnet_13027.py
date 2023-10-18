def build_clusters(data, sample, maxindels):
    """
    Combines information from .utemp and .htemp files to create .clust files,
    which contain un-aligned clusters. Hits to seeds are only kept in the
    cluster if the number of internal indels is less than 'maxindels'.
    By default, we set maxindels=6 for this step (within-sample clustering).
    """

    ## If reference assembly then here we're clustering the unmapped reads
    if "reference" in data.paramsdict["assembly_method"]:
        derepfile = os.path.join(data.dirs.edits, sample.name+"-refmap_derep.fastq")
    else:
        derepfile = os.path.join(data.dirs.edits, sample.name+"_derep.fastq")
    ## i/o vsearch files
    uhandle = os.path.join(data.dirs.clusts, sample.name+".utemp")
    usort = os.path.join(data.dirs.clusts, sample.name+".utemp.sort")
    hhandle = os.path.join(data.dirs.clusts, sample.name+".htemp")

    ## create an output file to write clusters to
    sample.files.clusters = os.path.join(data.dirs.clusts, sample.name+".clust.gz")
    clustsout = gzip.open(sample.files.clusters, 'wb')

    ## Sort the uhandle file so we can read through matches efficiently
    cmd = ["sort", "-k", "2", uhandle, "-o", usort]
    proc = sps.Popen(cmd, close_fds=True)
    _ = proc.communicate()[0]

    ## load ALL derep reads into a dictionary (this can be a few GB of RAM)
    ## and is larger if names are larger. We are grabbing two lines at a time.
    alldereps = {}
    with open(derepfile, 'rb') as ioderep:
        dereps = itertools.izip(*[iter(ioderep)]*2)
        for namestr, seq in dereps:
            nnn, sss = [i.strip() for i in namestr, seq]
            alldereps[nnn[1:]] = sss

    ## store observed seeds (this could count up to >million in bad data sets)
    seedsseen = set()

    ## Iterate through the usort file grabbing matches to build clusters
    with open(usort, 'rb') as insort:
        ## iterator, seed null, seqlist null
        isort = iter(insort)
        lastseed = 0
        fseqs = []
        seqlist = []
        seqsize = 0
        while 1:
            ## grab the next line
            try:
                hit, seed, _, ind, ori, _ = isort.next().strip().split()
                LOGGER.debug(">{} {} {}".format(hit, seed, ori, seq))
            except StopIteration:
                break

            ## same seed, append match
            if seed != lastseed:
                seedsseen.add(seed)
                ## store the last cluster (fseq), count it, and clear fseq
                if fseqs:
                    ## sort fseqs by derep after pulling out the seed
                    fseqs = [fseqs[0]] + sorted(fseqs[1:], key=lambda x: \
                        int(x.split(";size=")[1].split(";")[0]), reverse=True)                    
                    seqlist.append("\n".join(fseqs))
                    seqsize += 1
                    fseqs = []

                ## occasionally write/dump stored clusters to file and clear mem
                if not seqsize % 10000:
                    if seqlist:
                        clustsout.write("\n//\n//\n".join(seqlist)+"\n//\n//\n")
                        ## reset list and counter
                        seqlist = []

                ## store the new seed on top of fseq list
                fseqs.append(">{}*\n{}".format(seed, alldereps[seed]))
                lastseed = seed

            ## add match to the seed
            ## revcomp if orientation is reversed (comp preserves nnnn)
            if ori == "-":
                seq = comp(alldereps[hit])[::-1]
            else:
                seq = alldereps[hit]
            ## only save if not too many indels
            if int(ind) <= maxindels:
                fseqs.append(">{}{}\n{}".format(hit, ori, seq))
            else:
                LOGGER.info("filtered by maxindels: %s %s", ind, seq)

    ## write whatever is left over to the clusts file
    if fseqs:
        seqlist.append("\n".join(fseqs))
    if seqlist:
        clustsout.write("\n//\n//\n".join(seqlist)+"\n//\n//\n")

    ## now write the seeds that had no hits. Make dict from htemp
    with open(hhandle, 'rb') as iotemp:
        nohits = itertools.izip(*[iter(iotemp)]*2)
        seqlist = []
        seqsize = 0
        while 1:
            try:
                nnn, _ = [i.strip() for i in nohits.next()]
            except StopIteration:
                break

            ## occasionally write to file
            if not seqsize % 10000:
                if seqlist:
                    clustsout.write("\n//\n//\n".join(seqlist)+"\n//\n//\n")
                    ## reset list and counter
                    seqlist = []

            ## append to list if new seed
            if nnn[1:] not in seedsseen:
                seqlist.append("{}*\n{}".format(nnn, alldereps[nnn[1:]]))
                seqsize += 1

    ## write whatever is left over to the clusts file
    if seqlist:
        clustsout.write("\n//\n//\n".join(seqlist))#+"\n//\n//\n")

    ## close the file handle
    clustsout.close()
    del alldereps