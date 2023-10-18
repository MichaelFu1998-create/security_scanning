def concat_chunks(data, ipyclient):
    """ 
    Concatenate chunks. If multiple chunk files match to the same sample name
    but with different barcodes (i.e., they are technical replicates) then this
    will assign all the files to the same sample name file.
    """

    ## collate files progress bar
    start = time.time()
    printstr = ' writing/compressing   | {} | s1 |'
    lbview = ipyclient.load_balanced_view()
    elapsed = datetime.timedelta(seconds=int(time.time()-start))
    progressbar(10, 0, printstr.format(elapsed), spacer=data._spacer) 
    ## get all the files
    ftmps = glob.glob(os.path.join(data.dirs.fastqs, "tmp_*.fastq"))

    ## a dict to assign tmp files to names/reads
    r1dict = {}
    r2dict = {}
    for sname in data.barcodes:
        if "-technical-replicate-" in sname:
            sname = sname.rsplit("-technical-replicate", 1)[0]
        r1dict[sname] = []
        r2dict[sname] = []

    ## assign to name keys
    for ftmp in ftmps:
        base, orient, _ = ftmp.rsplit("_", 2)
        sname = base.rsplit("/", 1)[-1].split("tmp_", 1)[1]
        if orient == "R1":
            r1dict[sname].append(ftmp)
        else:
            r2dict[sname].append(ftmp)

    ## concatenate files
    snames = []
    for sname in data.barcodes:
        if "-technical-replicate-" in sname:
            sname = sname.rsplit("-technical-replicate", 1)[0]
        snames.append(sname)

    writers = []
    for sname in set(snames):
        tmp1s = sorted(r1dict[sname])
        tmp2s = sorted(r2dict[sname])
        writers.append(lbview.apply(collate_files, *[data, sname, tmp1s, tmp2s]))

    total = len(writers)
    while 1:
        ready = [i.ready() for i in writers]
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(total, sum(ready), printstr.format(elapsed), spacer=data._spacer) 
        time.sleep(0.1)
        if all(ready):
            print("")
            break