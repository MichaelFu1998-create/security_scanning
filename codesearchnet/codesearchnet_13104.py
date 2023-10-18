def merge_pairs(data, two_files, merged_out, revcomp, merge):
    """
    Merge PE reads. Takes in a list of unmerged files [r1, r2] and the
    filehandle to write merged data to, and it returns the number of reads
    that were merged (overlapping). If merge==0 then only concat pairs (nnnn),
    no merging in vsearch.

    Parameters
    -----------
    two_files (tuple):
        A list or tuple of the [r1, r2] files to be merged. 

    merged_out (str):
        A string file handle for the merged data to be written to. 

    revcomp (bool):
        Whether or not to revcomp the R2s. 

    merge (bool):
        Whether or not to perform vsearch merging. If not then reads are simply
        concatenated with a 'nnnn' separator. 

    Returns
    --------
    If merge is on then the func will return the number of pairs 
    successfully merged, else it returns -1. 
    """

    LOGGER.debug("Entering merge_pairs()")

    ## Return the number of merged pairs
    nmerged = -1

    ## Check input files from inside list-tuple [(r1, r2)]
    for fhandle in two_files[0]:
        if not os.path.exists(fhandle):
            raise IPyradWarningExit("""
    Attempting to merge a file that doesn't exist - {}""".format(fhandle))

    ## If it already exists, clean up the old merged file
    if os.path.exists(merged_out):
        os.remove(merged_out)

    ## if merge then catch nonmerged in a separate file
    if merge:
        nonmerged1 = tempfile.NamedTemporaryFile(mode='wb',
                                            dir=data.dirs.edits,
                                            suffix="_nonmerged_R1_.fastq").name
        nonmerged2 = tempfile.NamedTemporaryFile(mode='wb',
                                            dir=data.dirs.edits,
                                            suffix="_nonmerged_R2_.fastq").name

    ## if not merging then the nonmerged reads will come from the normal edits
    else:
        nonmerged1 = two_files[0][0]
        nonmerged2 = two_files[0][1]

    ## get the maxn and minlen values
    try:
        maxn = sum(data.paramsdict['max_low_qual_bases'])
    except TypeError:
        maxn = data.paramsdict['max_low_qual_bases']
    minlen = str(max(32, data.paramsdict["filter_min_trim_len"]))

    ## we need to gunzip the files if they are zipped (at least for now)
    if merge and two_files[0][0].endswith(".gz"):
        LOGGER.info("gunzipping pairs")
        tmp1 = os.path.splitext(two_files[0][0])[0]+".tmp1"
        tmp2 = os.path.splitext(two_files[0][1])[0]+".tmp2"

        out1 = open(tmp1, 'w')
        out2 = open(tmp2, 'w')
        gun1 = sps.Popen(["gunzip", "-c", two_files[0][0]],
                          stderr=sps.STDOUT, stdout=out1, close_fds=True)
        gun2 = sps.Popen(["gunzip", "-c", two_files[0][1]],
                          stderr=sps.STDOUT, stdout=out2, close_fds=True)
        _ = gun1.communicate()
        _ = gun2.communicate()
        out1.close()
        out2.close()
    else:
        tmp1 = two_files[0][0]
        tmp2 = two_files[0][1]
    try:
        ## If we are actually mergeing and not just joining then do vsearch
        if merge:
            ## create tmp files with high quality scores and with R2 oriented
            cmd = [ipyrad.bins.vsearch,
                   "--fastq_mergepairs", tmp1,
                   "--reverse", tmp2,
                   "--fastqout", merged_out,
                   "--fastqout_notmerged_fwd", nonmerged1,
                   "--fastqout_notmerged_rev", nonmerged2,
                   "--fasta_width", "0",
                   "--fastq_minmergelen", minlen,
                   "--fastq_maxns", str(maxn),
                   "--fastq_minovlen", "20",
                   "--fastq_maxdiffs", "4",
                   "--label_suffix", "_m1",
                   "--fastq_qmax", "1000",
                   "--threads", "2",
                   "--fastq_allowmergestagger"]

            LOGGER.debug("merge cmd: %s", " ".join(cmd))
            proc = sps.Popen(cmd, stderr=sps.STDOUT, stdout=sps.PIPE)
            try:
                res = proc.communicate()[0]
            except KeyboardInterrupt:
                proc.kill()

            if proc.returncode:
                LOGGER.error("Error: %s %s", cmd, res)
                ## remove temp files
                rmfiles = [os.path.splitext(two_files[0][0])[0]+".tmp1",
                           os.path.splitext(two_files[0][1])[0]+".tmp2",
                           nonmerged1, nonmerged2]
                for rmfile in rmfiles:
                    if os.path.exists(rmfile):
                        os.remove(rmfile)
                raise IPyradWarningExit("Error merge pairs:\n %s\n%s", cmd, res)

            ## record how many read pairs were merged
            with open(merged_out, 'r') as tmpf:
                #nmerged = len(tmpf.readlines()) // 4
                nmerged = sum(1 for i in tmpf.readlines()) // 4

        ## Combine the unmerged pairs and append to the merge file
        with open(merged_out, 'ab') as combout:
            ## read in paired end read files 4 lines at a time
            if nonmerged1.endswith(".gz"):
                fr1 = gzip.open(nonmerged1, 'rb')
            else:
                fr1 = open(nonmerged1, 'rb')
            quart1 = itertools.izip(*[iter(fr1)]*4)
            if nonmerged2.endswith(".gz"):
                fr2 = gzip.open(nonmerged2, 'rb')
            else:
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
                if revcomp:
                    writing.append("".join([
                        read1s[0],
                        read1s[1].strip() + "nnnn" + \
                        comp(read2s[1].strip()[::-1]) + "\n",
                        read1s[2],
                        read1s[3].strip() + "nnnn" + \
                        read2s[3].strip()[::-1] + "\n",
                        ]))
                else:
                    writing.append("".join([
                        read1s[0],
                        read1s[1].strip() + "nnnn" + \
                        read2s[1],
                        read1s[2],
                        read1s[3].strip() + "nnnn" + \
                        read2s[3],
                        ]))

                counts += 1
                if not counts % 10:
                    combout.write("".join(writing)) #+"\n")
                    writing = []

            if writing:
                combout.write("".join(writing))

        ## close handles
        fr1.close()
        fr2.close()
        combout.close()

    except Exception as inst:
        LOGGER.error("Exception in merge_pairs - {}".format(inst))
        raise
    ## No matter what happens please clean up the temp files.
    finally:
        ## if merged then delete the nonmerge tmp files
        if merge:
            ## remove temp files
            rmfiles = [nonmerged1, nonmerged2,
                       os.path.splitext(two_files[0][0])[0]+".tmp1",
                       os.path.splitext(two_files[0][1])[0]+".tmp2"]
            for rmfile in rmfiles:
                if os.path.exists(rmfile):
                    os.remove(rmfile)

    return nmerged