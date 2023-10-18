def trim_reference_sequence(fasta):
    """
    If doing PE and R1/R2 don't overlap then the reference sequence
    will be quite long and will cause indel hell during the 
    alignment stage. Here trim the reference sequence to the length
    of the merged reads. Input is a list of alternating locus labels
    and sequence data. The first locus label is the reference
    sequence label and the first seq is the reference seq. Returns
    the same list except with the reference sequence trimmed to
    the length of the rad tags
    """
    LOGGER.debug("pre - {}".format(fasta[0]))

    ## If the reads are merged then the reference sequence should be the
    ## same length as the merged pair. If unmerged then we have to fix it.
    if "nnnn" in fasta[1]:
        r1_len = len(fasta[1].split("\n")[1].split("nnnn")[0])
        r2_len = len(fasta[1].split("\n")[1].split("nnnn")[1])
        new_seq = fasta[0].split("\n")[1][:r1_len]+("nnnn")\
                    + revcomp(fasta[0].split("\n")[1][-r2_len:])
        fasta[0] = fasta[0].split("\n")[0]+"\n"+new_seq

    LOGGER.debug("post - {}".format(fasta[0]))
    return fasta