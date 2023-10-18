def concat_multiple_edits(data, sample):
    """
    if multiple fastq files were appended into the list of fastqs for samples
    then we merge them here before proceeding.
    """

    ## if more than one tuple in fastq list
    if len(sample.files.edits) > 1:
        ## create a cat command to append them all (doesn't matter if they
        ## are gzipped, cat still works). Grab index 0 of tuples for R1s.
        cmd1 = ["cat"] + [i[0] for i in sample.files.edits]

        ## write to new concat handle
        conc1 = os.path.join(data.dirs.edits, sample.name+"_R1_concatedit.fq.gz")
        with open(conc1, 'w') as cout1:
            proc1 = sps.Popen(cmd1, stderr=sps.STDOUT, stdout=cout1, close_fds=True)
            res1 = proc1.communicate()[0]
        if proc1.returncode:
            raise IPyradWarningExit("error in: %s, %s", cmd1, res1)

        ## Only set conc2 if R2 actually exists
        conc2 = 0
        if os.path.exists(str(sample.files.edits[0][1])):
            cmd2 = ["cat"] + [i[1] for i in sample.files.edits]
            conc2 = os.path.join(data.dirs.edits, sample.name+"_R2_concatedit.fq.gz")
            with gzip.open(conc2, 'w') as cout2:
                proc2 = sps.Popen(cmd2, stderr=sps.STDOUT, stdout=cout2, close_fds=True)
                res2 = proc2.communicate()[0]
            if proc2.returncode:
                raise IPyradWarningExit("error in: %s, %s", cmd2, res2)

        ## store new file handles
        sample.files.edits = [(conc1, conc2)]
    return sample.files.edits