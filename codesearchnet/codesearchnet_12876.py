def writetofastq(data, dsort, read):
    """ 
    Writes sorted data 'dsort dict' to a tmp files
    """
    if read == 1:
        rrr = "R1"
    else:
        rrr = "R2"

    for sname in dsort:
        ## skip writing if empty. Write to tmpname
        handle = os.path.join(data.dirs.fastqs, 
                "{}_{}_.fastq".format(sname, rrr))
        with open(handle, 'a') as out:
            out.write("".join(dsort[sname]))