def derep_concat_split(data, sample, nthreads, force):
    """
    Running on remote Engine. Refmaps, then merges, then dereplicates,
    then denovo clusters reads.
    """

    ## report location for debugging
    LOGGER.info("INSIDE derep %s", sample.name)

    ## MERGED ASSEMBIES ONLY:
    ## concatenate edits files within Samples. Returns a new sample.files.edits 
    ## with the concat file. No change if not merged Assembly.
    mergefile = os.path.join(data.dirs.edits, sample.name+"_merged_.fastq")
    if not force:
        if not os.path.exists(mergefile):
            sample.files.edits = concat_multiple_edits(data, sample)
        else:
            LOGGER.info("skipped concat_multiple_edits: {} exists"\
                        .format(mergefile))
    else:
        sample.files.edits = concat_multiple_edits(data, sample)

    ## PAIRED DATA ONLY:
    ## Denovo: merge or concat fastq pairs [sample.files.pairs]
    ## Reference: only concat fastq pairs  []
    ## Denovo + Reference: ...
    if 'pair' in data.paramsdict['datatype']:
        ## the output file handle for merged reads
        

        ## modify behavior of merging vs concating if reference
        if "reference" in data.paramsdict["assembly_method"]:
            nmerged = merge_pairs(data, sample.files.edits, mergefile, 0, 0)
        else:
            nmerged = merge_pairs(data, sample.files.edits, mergefile, 1, 1)

        ## store results
        sample.files.edits = [(mergefile, )]
        sample.stats.reads_merged = nmerged

    ## 3rad uses random adapters to identify pcr duplicates. We will
    ## remove pcr dupes here. Basically append the radom adapter to
    ## each sequence, do a regular old vsearch derep, then trim
    ## off the adapter, and push it down the pipeline. This will
    ## remove all identical seqs with identical random i5 adapters.
    if "3rad" in data.paramsdict["datatype"]:
        declone_3rad(data, sample)
        derep_and_sort(data,
                os.path.join(data.dirs.edits, sample.name+"_declone.fastq"),
                os.path.join(data.dirs.edits, sample.name+"_derep.fastq"),
                nthreads)
    else:
        ## convert fastq to fasta, then derep and sort reads by their size.
        ## we pass in only one file b/c paired should be merged by now.
        derep_and_sort(data,
                sample.files.edits[0][0],
                os.path.join(data.dirs.edits, sample.name+"_derep.fastq"),
                nthreads)