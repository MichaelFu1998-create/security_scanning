def fetch_cluster_se(data, samfile, chrom, rstart, rend):
    """
    Builds a single end cluster from the refmapped data.
    """

    ## If SE then we enforce the minimum overlap distance to avoid the
    ## staircase syndrome of multiple reads overlapping just a little.
    overlap_buffer = data._hackersonly["min_SE_refmap_overlap"]

    ## the *_buff variables here are because we have to play patty
    ## cake here with the rstart/rend vals because we want pysam to
    ## enforce the buffer for SE, but we want the reference sequence
    ## start and end positions to print correctly for downstream.
    rstart_buff = rstart + overlap_buffer
    rend_buff = rend - overlap_buffer

    ## Reads that map to only very short segements of the reference
    ## sequence will return buffer end values that are before the
    ## start values causing pysam to complain. Very short mappings.
    if rstart_buff > rend_buff:
        tmp = rstart_buff
        rstart_buff = rend_buff
        rend_buff = tmp
    ## Buffering can't make start and end equal or pysam returns nothing.
    if rstart_buff == rend_buff:
        rend_buff += 1

    ## store pairs
    rdict = {}
    clust = []
    iterreg = []

    iterreg = samfile.fetch(chrom, rstart_buff, rend_buff)

    ## use dict to match up read pairs
    for read in iterreg:
        if read.qname not in rdict:
            rdict[read.qname] = read

    ## sort dict keys so highest derep is first ('seed')
    sfunc = lambda x: int(x.split(";size=")[1].split(";")[0])
    rkeys = sorted(rdict.keys(), key=sfunc, reverse=True)

    ## get blocks from the seed for filtering, bail out if seed is not paired
    try:
        read1 = rdict[rkeys[0]]
    except ValueError:
        LOGGER.error("Found bad cluster, skipping - key:{} rdict:{}".format(rkeys[0], rdict))
        return ""

    ## the starting blocks for the seed
    poss = read1.get_reference_positions(full_length=True)
    seed_r1start = min(poss)
    seed_r1end = max(poss)

    ## store the seed -------------------------------------------
    if read1.is_reverse:
        seq = revcomp(read1.seq)
    else:
        seq = read1.seq

    ## store, could write orient but just + for now.
    size = sfunc(rkeys[0])
    clust.append(">{}:{}:{};size={};*\n{}"\
        .format(chrom, seed_r1start, seed_r1end, size, seq))

    ## If there's only one hit in this region then rkeys will only have
    ## one element and the call to `rkeys[1:]` will raise. Test for this.
    if len(rkeys) > 1:
        ## store the hits to the seed -------------------------------
        for key in rkeys[1:]:
            skip = False
            try:
                read1 = rdict[key]
            except ValueError:
                ## enter values that will make this read get skipped
                read1 = rdict[key][0]
                skip = True

            ## orient reads only if not skipping
            if not skip:
                poss = read1.get_reference_positions(full_length=True)
                minpos = min(poss)
                maxpos = max(poss)
                ## store the seq
                if read1.is_reverse:
                    seq = revcomp(read1.seq)
                else:
                    seq = read1.seq
                ## store, could write orient but just + for now.
                size = sfunc(key)
                clust.append(">{}:{}:{};size={};+\n{}"\
                    .format(chrom, minpos, maxpos, size, seq))
            else:
                ## seq is excluded, though, we could save it and return
                ## it as a separate cluster that will be aligned separately.
                pass

    return clust