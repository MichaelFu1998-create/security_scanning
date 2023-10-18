def refmap_stats(data, sample):
    """ 
    Get the number of mapped and unmapped reads for a sample
    and update sample.stats 
    """
    ## shorter names
    mapf = os.path.join(data.dirs.refmapping, sample.name+"-mapped-sorted.bam")
    umapf = os.path.join(data.dirs.refmapping, sample.name+"-unmapped.bam")

    ## get from unmapped
    cmd1 = [ipyrad.bins.samtools, "flagstat", umapf]
    proc1 = sps.Popen(cmd1, stderr=sps.STDOUT, stdout=sps.PIPE)
    result1 = proc1.communicate()[0]

    ## get from mapped
    cmd2 = [ipyrad.bins.samtools, "flagstat", mapf]
    proc2 = sps.Popen(cmd2, stderr=sps.STDOUT, stdout=sps.PIPE)
    result2 = proc2.communicate()[0]

    ## store results
    ## If PE, samtools reports the _actual_ number of reads mapped, both 
    ## R1 and R2, so here if PE divide the results by 2 to stay consistent
    ## with how we've been reporting R1 and R2 as one "read pair"
    if "pair" in data.paramsdict["datatype"]:
        sample.stats["refseq_unmapped_reads"] = int(result1.split()[0]) / 2
        sample.stats["refseq_mapped_reads"] = int(result2.split()[0]) / 2
    else:
        sample.stats["refseq_unmapped_reads"] = int(result1.split()[0])
        sample.stats["refseq_mapped_reads"] = int(result2.split()[0])

    sample_cleanup(data, sample)