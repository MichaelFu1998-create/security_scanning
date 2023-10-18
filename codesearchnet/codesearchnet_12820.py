def bedtools_merge(data, sample):
    """ 
    Get all contiguous genomic regions with one or more overlapping
    reads. This is the shell command we'll eventually run

    bedtools bamtobed -i 1A_0.sorted.bam | bedtools merge [-d 100]
        -i <input_bam>  :   specifies the input file to bed'ize
        -d <int>        :   For PE set max distance between reads
    """
    LOGGER.info("Entering bedtools_merge: %s", sample.name)
    mappedreads = os.path.join(data.dirs.refmapping, 
                               sample.name+"-mapped-sorted.bam")

    ## command to call `bedtools bamtobed`, and pipe output to stdout
    ## Usage:   bedtools bamtobed [OPTIONS] -i <bam> 
    ## Usage:   bedtools merge [OPTIONS] -i <bam> 
    cmd1 = [ipyrad.bins.bedtools, "bamtobed", "-i", mappedreads]
    cmd2 = [ipyrad.bins.bedtools, "merge", "-i", "-"]

    ## If PE the -d flag to tell bedtools how far apart to allow mate pairs.
    ## If SE the -d flag is negative, specifying that SE reads need to
    ## overlap by at least a specific number of bp. This prevents the
    ## stairstep syndrome when a + and - read are both extending from
    ## the same cutsite. Passing a negative number to `merge -d` gets this done.
    if 'pair' in data.paramsdict["datatype"]:
        check_insert_size(data, sample)
        #cmd2.insert(2, str(data._hackersonly["max_inner_mate_distance"]))
        cmd2.insert(2, str(data._hackersonly["max_inner_mate_distance"]))
        cmd2.insert(2, "-d")
    else:
        cmd2.insert(2, str(-1 * data._hackersonly["min_SE_refmap_overlap"]))
        cmd2.insert(2, "-d")

    ## pipe output from bamtobed into merge
    LOGGER.info("stdv: bedtools merge cmds: %s %s", cmd1, cmd2)
    proc1 = sps.Popen(cmd1, stderr=sps.STDOUT, stdout=sps.PIPE)
    proc2 = sps.Popen(cmd2, stderr=sps.STDOUT, stdout=sps.PIPE, stdin=proc1.stdout)
    result = proc2.communicate()[0]
    proc1.stdout.close()

    ## check for errors and do cleanup
    if proc2.returncode:
        raise IPyradWarningExit("error in %s: %s", cmd2, result)

    ## Write the bedfile out, because it's useful sometimes.
    if os.path.exists(ipyrad.__debugflag__):
        with open(os.path.join(data.dirs.refmapping, sample.name + ".bed"), 'w') as outfile:
            outfile.write(result)

    ## Report the number of regions we're returning
    nregions = len(result.strip().split("\n"))
    LOGGER.info("bedtools_merge: Got # regions: %s", nregions)
    return result