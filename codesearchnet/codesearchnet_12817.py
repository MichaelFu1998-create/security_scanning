def get_overlapping_reads(data, sample, regions):
    """
    For SE data, this pulls mapped reads out of sorted mapped bam files and 
    appends them to the clust.gz file so they fall into downstream 
    (muscle alignment) analysis. 

    For PE data, this pulls mapped reads out of sorted mapped bam files, splits 
    R1s from R2s and writes them to separate files. Once all reads are written, 
    it calls merge_reads (vsearch) to find merged and non-merged reads. These
    are then put into clust.gz with either an nnnn separator or as merged. 
    
    The main func being called here is 'bam_region_to_fasta', which calls
    samtools to pull out the mapped reads. 

    1) Coming into this function we have sample.files.mapped_reads 
        as a sorted bam file, and a passed in list of regions to evaluate.
    2) Get all reads overlapping with each individual region.
    3) Pipe to vsearch for clustering.
    4) Append to the clust.gz file.
    """

    ## storage and counter
    locus_list = []
    reads_merged = 0

    ## Set the write mode for opening clusters file.
    ## 1) if "reference" then only keep refmapped, so use 'wb' to overwrite 
    ## 2) if "denovo+reference" then 'ab' adds to end of denovo clust file
    write_flag = 'wb'
    if data.paramsdict["assembly_method"] == "denovo+reference":
        write_flag = 'ab'

    ## file handle for writing clusters
    sample.files.clusters = os.path.join(data.dirs.clusts, sample.name+".clust.gz")
    outfile = gzip.open(sample.files.clusters, write_flag)

    ## write a separator if appending to clust.gz
    if data.paramsdict["assembly_method"] == "denovo+reference":
        outfile.write("\n//\n//\n")

    ## Make a process to pass in to bam_region_to_fasta so we can just reuse
    ## it rather than recreating a bunch of subprocesses. Saves hella time.
    proc1 = sps.Popen("sh", stdin=sps.PIPE, stdout=sps.PIPE, universal_newlines=True)

    # Wrap this in a try so we can easily locate errors
    try:
        ## For each identified region, build the pileup and write out the fasta
        for line in regions.strip().split("\n"):

            # Blank lines returned from bedtools screw things up. Filter them.
            if line == "":
                continue

            ## get elements from bedtools region
            chrom, region_start, region_end = line.strip().split()[0:3]

            ## bam_region_to_fasta returns a chunk of fasta sequence
            args = [data, sample, proc1, chrom, region_start, region_end]
            clust = bam_region_to_fasta(*args)

            ## If bam_region_to_fasta fails for some reason it'll return [], 
            ## in which case skip the rest of this. Normally happens if reads
            ## map successfully, but too far apart.
            if not clust:
                continue

            ## Store locus in a list
            # LOGGER.info("clust from bam-region-to-fasta \n %s", clust)
            locus_list.append(clust)

            ## write chunk of 1000 loci and clear list to minimize memory
            if not len(locus_list) % 1000:
                outfile.write("\n//\n//\n".join(locus_list)+"\n//\n//\n")
                locus_list = []
        
        ## write remaining
        if any(locus_list):
            outfile.write("\n//\n//\n".join(locus_list))
        else:
            ## If it's empty, strip off the last \n//\n//\n from the outfile.
            pass

        ## close handle
        outfile.close()

    except Exception as inst:
        LOGGER.error("Exception inside get_overlapping_reads - {}".format(inst))
        raise

    finally:
        if "pair" in data.paramsdict["datatype"]:
            LOGGER.info("Total merged reads for {} - {}"\
                     .format(sample.name, reads_merged))
            sample.stats.reads_merged = reads_merged