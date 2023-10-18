def check_insert_size(data, sample):
    """
    check mean insert size for this sample and update 
    hackersonly.max_inner_mate_distance if need be. This value controls how 
    far apart mate pairs can be to still be considered for bedtools merging 
    downstream.
    """

    ## pipe stats output to grep
    cmd1 = [ipyrad.bins.samtools, "stats", sample.files.mapped_reads]
    cmd2 = ["grep", "SN"]
    proc1 = sps.Popen(cmd1, stderr=sps.STDOUT, stdout=sps.PIPE)
    proc2 = sps.Popen(cmd2, stderr=sps.STDOUT, stdout=sps.PIPE, stdin=proc1.stdout)

    ## get piped result
    res = proc2.communicate()[0]

    ## raise exception on failure and do cleanup
    if proc2.returncode:
        raise IPyradWarningExit("error in %s: %s", cmd2, res)
        
    ## starting vals
    avg_insert = 0
    stdv_insert = 0
    avg_len = 0

    ## iterate over results
    for line in res.split("\n"):
        if "insert size average" in line:
            avg_insert = float(line.split(":")[-1].strip())

        elif "insert size standard deviation" in line:
            ## hack to fix sim data when stdv is 0.0. Shouldn't
            ## impact real data bcz stdv gets rounded up below
            stdv_insert = float(line.split(":")[-1].strip()) + 0.1
       
        elif "average length" in line:
            avg_len = float(line.split(":")[-1].strip())

    LOGGER.debug("avg {} stdv {} avg_len {}"\
                 .format(avg_insert, stdv_insert, avg_len))

    ## If all values return successfully set the max inner mate distance.
    ## This is tricky. avg_insert is the average length of R1+R2+inner mate
    ## distance. avg_len is the average length of a read. If there are lots
    ## of reads that overlap then avg_insert will be close to but bigger than
    ## avg_len. We are looking for the right value for `bedtools merge -d`
    ## which wants to know the max distance between reads. 
    if all([avg_insert, stdv_insert, avg_len]):
        ## If 2 * the average length of a read is less than the average
        ## insert size then most reads DO NOT overlap
        if stdv_insert < 5:
            stdv_insert = 5.
        if (2 * avg_len) < avg_insert:
            hack = avg_insert + (3 * np.math.ceil(stdv_insert)) - (2 * avg_len)

        ## If it is > than the average insert size then most reads DO
        ## overlap, so we have to calculate inner mate distance a little 
        ## differently.
        else:
            hack = (avg_insert - avg_len) + (3 * np.math.ceil(stdv_insert))
            

        ## set the hackerdict value
        LOGGER.info("stdv: hacked insert size is %s", hack)
        data._hackersonly["max_inner_mate_distance"] = int(np.math.ceil(hack))

    else:
        ## If something fsck then set a relatively conservative distance
        data._hackersonly["max_inner_mate_distance"] = 300
        LOGGER.debug("inner mate distance for {} - {}".format(sample.name,\
                    data._hackersonly["max_inner_mate_distance"]))