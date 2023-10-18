def merge_pairs_after_refmapping(data, two_files, merged_out):
    """ 
    A function to merge fastq files produced by bam2fq.
    """

    ## create temp files 
    nonmerged1 = tempfile.NamedTemporaryFile(
        mode='wb',
        dir=data.dirs.edits,
        suffix="_nonmerged_R1_.fastq").name
    nonmerged2 = tempfile.NamedTemporaryFile(
        mode='wb',
        dir=data.dirs.edits,
        suffix="_nonmerged_R2_.fastq").name 

    ## get the maxn and minlen values
    minlen = str(max(32, data.paramsdict["filter_min_trim_len"]))
    try:
        maxn = sum(data.paramsdict['max_low_qual_bases'])
    except TypeError:
        maxn = data.paramsdict['max_low_qual_bases']
 
    ## set the quality scores abritrarily high and orient R2 correctly
    tmp1 = two_files[0][0]
    tmp2 = two_files[0][1]
    fastq_touchup_for_vsearch_merge(tmp1, tmp1+".tu", False)
    fastq_touchup_for_vsearch_merge(tmp2, tmp2+".tu", True)

    ## command string to call vsearch
    cmd = [ipyrad.bins.vsearch,
           "--fastq_mergepairs", tmp1+".tu",
           "--reverse", tmp2+".tu",
           "--fastqout", merged_out,
           "--fastqout_notmerged_fwd", nonmerged1,
           "--fastqout_notmerged_rev", nonmerged2,
           "--fasta_width", "0",
           "--fastq_minmergelen", minlen,
           "--fastq_maxns", str(maxn),
           "--fastq_minovlen", "10",
           "--fastq_maxdiffs", "4",
           "--label_suffix", "_m1",
           "--fastq_qmax", "1000",
           "--threads", "2",
           "--fastq_allowmergestagger"]
    
    ## run vsearch but allow kbd
    proc = sps.Popen(cmd, stderr=sps.STDOUT, stdout=sps.PIPE)
    try:
        res = proc.communicate()[0]
    except KeyboardInterrupt:
        proc.kill()

    ## cleanup tmp files if job failed or stopped    
    if proc.returncode:
        LOGGER.error("Error: %s %s", cmd, res)
        raise IPyradWarningExit("Error merge pairs:\n %s\n%s", cmd, res)

    ## record how many read pairs were merged
    with open(merged_out, 'r') as tmpf:
        nmerged = sum(1 for i in tmpf.readlines()) // 4

    ## Concat unmerged pairs with a 'nnnn' separator
    with open(merged_out, 'ab') as combout:
        ## read in paired end read files 4 lines at a time
        fr1 = open(nonmerged1, 'rb')
        quart1 = itertools.izip(*[iter(fr1)]*4)
        fr2 = open(nonmerged2, 'rb')
        quart2 = itertools.izip(*[iter(fr2)]*4)
        quarts = itertools.izip(quart1, quart2)

        ## a list to store until writing
        writing = []
        counts = 0

        ## iterate until done
        while 1:
            try:
                read1s, read2s = quarts.next()
            except StopIteration:
                break

            ## store the read
            writing.append("".join([
                read1s[0],
                read1s[1].strip() + "nnnn" + \
                read2s[1], 
                read1s[2],
                read1s[3].strip() + "nnnn" + \
                read2s[3], 
                ]))

            ## count up until time to write
            counts += 1
            if not counts % 10:
                combout.write("".join(writing))
                writing = []
        ## write the remaining
        if writing:
            combout.write("".join(writing))

        ## close handles
        fr1.close()
        fr2.close()
        combout.close()

    ## remove temp files (or do this later)
    rmfiles = [nonmerged1, nonmerged2, tmp1, tmp2, tmp1+".tu", tmp2+".tu"]
    for rmfile in rmfiles:
        if os.path.exists(rmfile):
            os.remove(rmfile)

    return nmerged