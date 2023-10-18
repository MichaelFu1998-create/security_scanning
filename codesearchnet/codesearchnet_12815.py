def ref_build_and_muscle_chunk(data, sample):
    """ 
    1. Run bedtools to get all overlapping regions
    2. Parse out reads from regions using pysam and dump into chunk files. 
       We measure it out to create 10 chunk files per sample. 
    3. If we really wanted to speed this up, though it is pretty fast already, 
       we could parallelize it since we can easily break the regions into 
       a list of chunks. 
    """

    ## get regions using bedtools
    regions = bedtools_merge(data, sample).strip().split("\n")
    nregions = len(regions)
    chunksize = (nregions / 10) + (nregions % 10)

    LOGGER.debug("nregions {} chunksize {}".format(nregions, chunksize))
    ## create an output file to write clusters to
    idx = 0
    tmpfile = os.path.join(data.tmpdir, sample.name+"_chunk_{}.ali")
    ## remove old files if they exist to avoid append errors
    for i in range(11):
        if os.path.exists(tmpfile.format(i)):
            os.remove(tmpfile.format(i))
    fopen = open

    ## If reference+denovo we drop the reads back into clust.gz
    ## and let the muscle_chunker do it's thing back in cluster_within
    if data.paramsdict["assembly_method"] == "denovo+reference":
        tmpfile = os.path.join(data.dirs.clusts, sample.name+".clust.gz")
        fopen = gzip.open
    
    ## build clusters for aligning with muscle from the sorted bam file
    samfile = pysam.AlignmentFile(sample.files.mapped_reads, 'rb')
    #"./tortas_refmapping/PZ70-mapped-sorted.bam", "rb")

    ## fill clusts list and dump periodically
    clusts = []
    nclusts = 0
    for region in regions:
        chrom, pos1, pos2 = region.split()
        try:
            ## fetches pairs quickly but then goes slow to merge them.
            if "pair" in data.paramsdict["datatype"]:
                clust = fetch_cluster_pairs(data, samfile, chrom, int(pos1), int(pos2))

            ## fetch but no need to merge
            else:
                clust = fetch_cluster_se(data, samfile, chrom, int(pos1), int(pos2))
        except IndexError as inst:
            LOGGER.error("Bad region chrom:start-end {}:{}-{}".format(chrom, pos1, pos2))
            continue
        if clust:
            clusts.append("\n".join(clust))
            nclusts += 1

            if nclusts == chunksize:
                ## write to file
                tmphandle = tmpfile.format(idx)
                with fopen(tmphandle, 'a') as tmp:
                    #LOGGER.debug("Writing tmpfile - {}".format(tmpfile.format(idx)))
                    #if data.paramsdict["assembly_method"] == "denovo+reference":
                    #    ## This is dumb, but for this method you need to prepend the
                    #    ## separator to maintain proper formatting of clust.gz
                    tmp.write("\n//\n//\n".join(clusts)+"\n//\n//\n")
                idx += 1
                nclusts = 0
                clusts = []
    if clusts:
        ## write remaining to file
        with fopen(tmpfile.format(idx), 'a') as tmp:
            #tmp.write("\n//\n//\n" + ("\n//\n//\n".join(clusts)))
            tmp.write("\n//\n//\n".join(clusts)+"\n//\n//\n")
        clusts = []
    
    if not data.paramsdict["assembly_method"] == "denovo+reference":
        chunkfiles = glob.glob(os.path.join(data.tmpdir, sample.name+"_chunk_*.ali"))
        LOGGER.info("created chunks %s", chunkfiles)

    ## cleanup
    samfile.close()