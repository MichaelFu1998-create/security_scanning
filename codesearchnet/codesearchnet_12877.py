def collate_files(data, sname, tmp1s, tmp2s):
    """ 
    Collate temp fastq files in tmp-dir into 1 gzipped sample.
    """
    ## out handle
    out1 = os.path.join(data.dirs.fastqs, "{}_R1_.fastq.gz".format(sname))
    out = io.BufferedWriter(gzip.open(out1, 'w'))

    ## build cmd
    cmd1 = ['cat']
    for tmpfile in tmp1s:
        cmd1 += [tmpfile]

    ## compression function
    proc = sps.Popen(['which', 'pigz'], stderr=sps.PIPE, stdout=sps.PIPE).communicate()
    if proc[0].strip():
        compress = ["pigz"]
    else:
        compress = ["gzip"]

    ## call cmd
    proc1 = sps.Popen(cmd1, stderr=sps.PIPE, stdout=sps.PIPE)
    proc2 = sps.Popen(compress, stdin=proc1.stdout, stderr=sps.PIPE, stdout=out)
    err = proc2.communicate()
    if proc2.returncode:
        raise IPyradWarningExit("error in collate_files R1 %s", err)
    proc1.stdout.close()
    out.close()

    ## then cleanup
    for tmpfile in tmp1s:
        os.remove(tmpfile)

    if 'pair' in data.paramsdict["datatype"]:
        ## out handle
        out2 = os.path.join(data.dirs.fastqs, "{}_R2_.fastq.gz".format(sname))
        out = io.BufferedWriter(gzip.open(out2, 'w'))

        ## build cmd
        cmd1 = ['cat']
        for tmpfile in tmp2s:
            cmd1 += [tmpfile]

        ## call cmd
        proc1 = sps.Popen(cmd1, stderr=sps.PIPE, stdout=sps.PIPE)
        proc2 = sps.Popen(compress, stdin=proc1.stdout, stderr=sps.PIPE, stdout=out)
        err = proc2.communicate()
        if proc2.returncode:
            raise IPyradWarningExit("error in collate_files R2 %s", err)
        proc1.stdout.close()
        out.close()

        ## then cleanup
        for tmpfile in tmp2s:
            os.remove(tmpfile)