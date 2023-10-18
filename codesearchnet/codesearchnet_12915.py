def build_indels(data, samples, ipyclient):
    """
    Builds the indels array and catclust.gz file from the aligned clusters.
    Building catclust is very fast. Entering indels into h5 array is a bit
    slow but can probably be sped up. (todo). NOT currently parallelized.
    """

    ## progress bars
    lbview = ipyclient.load_balanced_view()
    start = time.time()
    printstr = " database indels       | {} | s6 |"
    njobs = len(glob.glob(os.path.join(data.tmpdir, "align_*.fa"))) + 1

    ## build tmparrs
    async = lbview.apply(build_tmp_h5, *(data, samples))

    ## track progress
    while 1:
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        ready = bool(async.ready())
        progressbar(njobs, ready, printstr.format(elapsed), spacer=data._spacer)
        if ready:
            break
        else:
            time.sleep(0.1)

    ## check for errors
    if not async.successful():
        raise IPyradWarningExit(async.result())

    ## start subfunc
    async = lbview.apply(sub_build_indels, *(data, samples))
    
    prog = 1
    while 1:
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        if async.stdout:
            prog = int(async.stdout.split()[-1])+1
        progressbar(njobs, prog, printstr.format(elapsed), spacer=data._spacer)
        if async.ready():
            break
        else:
            time.sleep(0.1)

    ## check for errors
    if not async.successful():
        raise IPyradWarningExit(async.result())
    print("")

    ## prepare for next substep by removing the singlecat result files if 
    ## they exist. 
    snames = [i.name for i in samples]
    snames.sort()
    smpios = [os.path.join(data.dirs.across, i+'.tmp.h5') for i in snames]
    for smpio in smpios:
        if os.path.exists(smpio):
            os.remove(smpio)