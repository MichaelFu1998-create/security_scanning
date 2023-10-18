def fetch_cluster_pairs(data, samfile, chrom, rstart, rend):
    """ 
    Builds a paired cluster from the refmapped data.
    """
    ## store pairs
    rdict = {}
    clust = []

    ## grab the region and make tuples of info
    iterreg = samfile.fetch(chrom, rstart, rend)

    ## use dict to match up read pairs
    for read in iterreg:
        if read.qname not in rdict:
            rdict[read.qname] = [read]
        else:
            rdict[read.qname].append(read)

    ## sort dict keys so highest derep is first ('seed')
    sfunc = lambda x: int(x.split(";size=")[1].split(";")[0])
    rkeys = sorted(rdict.keys(), key=sfunc, reverse=True)
    
    ## get blocks from the seed for filtering, bail out if seed is not paired
    try:
        read1, read2 = rdict[rkeys[0]]
    except ValueError:
        return 0

    ## the starting blocks for the seed
    poss = read1.get_reference_positions() + read2.get_reference_positions()
    seed_r1start = min(poss)
    seed_r2end = max(poss)

    ## store the seed -------------------------------------------
    ## Simplify. R1 and R2 are always on opposite strands, but the
    ## orientation is variable. We revcomp and order the reads to
    ## preserve genomic order.
    reads_overlap = False
    if read1.is_reverse:
        if read2.aend > read1.get_blocks()[0][0]:
            reads_overlap = True
            seq = read2.seq + "nnnn" + revcomp(read1.seq)
        else:
            seq = read2.seq + "nnnn" + read1.seq
    else:
        if read1.aend > read2.get_blocks()[0][0]:
            reads_overlap = True
            seq = read1.seq + "nnnn" + revcomp(read2.seq)
        else:
            seq = read1.seq + "nnnn" + read2.seq

    ## store, could write orient but just + for now.
    size = sfunc(rkeys[0])
    clust.append(">{}:{}:{};size={};*\n{}"\
        .format(chrom, seed_r1start, seed_r2end, size, seq))

    ## If there's only one hit in this region then rkeys will only have
    ## one element and the call to `rkeys[1:]` will raise. Test for this.
    if len(rkeys) > 1:
        ## store the hits to the seed -------------------------------
        for key in rkeys[1:]:
            skip = False
            try:
                read1, read2 = rdict[key]
            except ValueError:
                ## enter values that will make this read get skipped
                read1 = rdict[key][0]
                read2 = read1
                skip = True

            ## orient reads and filter out ones that will not align well b/c
            ## they do not overlap enough with the seed
            poss = read1.get_reference_positions() + read2.get_reference_positions()
            minpos = min(poss)
            maxpos = max(poss)

            ## skip if more than one hit location
            if read1.has_tag("SA") or read2.has_tag("SA"):
                skip = True

            ## store if read passes 
            if (abs(minpos - seed_r1start) < 50) and \
               (abs(maxpos - seed_r2end) < 50) and \
               (not skip):
                ## store the seq
                if read1.is_reverse:
                    ## do reads overlap
                    if read2.aend > read1.get_blocks()[0][0]:
                        reads_overlap = True
                        seq = read2.seq + "nnnn" + revcomp(read1.seq)
                    else:
                        seq = read2.seq + "nnnn" + read1.seq
                else:
                    if read1.aend > read2.get_blocks()[0][0]:
                        reads_overlap = True
                        seq = read1.seq + "nnnn" + revcomp(read2.seq)
                    else:
                        seq = read1.seq + "nnnn" + read2.seq

                ## store, could write orient but just + for now.
                size = sfunc(key)
                clust.append(">{}:{}:{};size={};+\n{}"\
                    .format(chrom, minpos, maxpos, size, seq))
            else:
                ## seq is excluded, though, we could save it and return
                ## it as a separate cluster that will be aligned separately.
                pass

    ## merge the pairs prior to returning them
    ## Remember, we already tested for quality scores, so
    ## merge_after_pysam will generate arbitrarily high scores
    ## It would be nice to do something here like test if
    ## the average insert length + 2 stdv is > 2*read len
    ## so you can switch off merging for mostly non-overlapping data
    if reads_overlap:
        if data._hackersonly["refmap_merge_PE"]:
            clust = merge_after_pysam(data, clust)
            #clust = merge_pair_pipes(data, clust)

    return clust