def ref_muscle_chunker(data, sample):
    """ 
    Run bedtools to get all overlapping regions. Pass this list into the func
    'get_overlapping_reads' which will write fastq chunks to the clust.gz file.

    1) Run bedtools merge to get a list of all contiguous blocks of bases
    in the reference seqeunce where one or more of our reads overlap.
    The output will look like this:
            1       45230754        45230783
            1       74956568        74956596
            ...
            1       116202035       116202060
    """
    LOGGER.info('entering ref_muscle_chunker')

    ## Get regions, which will be a giant list of 5-tuples, of which we're 
    ## only really interested in the first three: (chrom, start, end) position.
    regions = bedtools_merge(data, sample)

    if len(regions) > 0:
        ## this calls bam_region_to_fasta a billion times
        get_overlapping_reads(data, sample, regions)
    else:
        msg = "No reads mapped to reference sequence - {}".format(sample.name)
        LOGGER.warn(msg)