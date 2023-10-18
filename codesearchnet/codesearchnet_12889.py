def zcat_make_temps(data, raws, num, tmpdir, optim, njobs, start):
    """ 
    Call bash command 'cat' and 'split' to split large files. The goal
    is to create N splitfiles where N is a multiple of the number of processors
    so that each processor can work on a file in parallel.
    """

    printstr = ' chunking large files  | {} | s1 |'

    ## split args
    tmpdir = os.path.realpath(tmpdir)
    LOGGER.info("zcat is using optim = %s", optim)

    ## read it, is it gzipped?
    catcmd = ["cat"]
    if raws[0].endswith(".gz"):
        catcmd = ["gunzip", "-c"]

    ## get reading commands for r1s, r2s
    cmd1 = catcmd + [raws[0]]
    cmd2 = catcmd + [raws[1]]

    ## second command splits and writes with name prefix
    cmd3 = ["split", "-a", "4", "-l", str(int(optim)), "-", 
            os.path.join(tmpdir, "chunk1_"+str(num)+"_")]
    cmd4 = ["split", "-a", "4", "-l", str(int(optim)), "-", 
            os.path.join(tmpdir, "chunk2_"+str(num)+"_")]

    ### run splitter
    proc1 = sps.Popen(cmd1, stderr=sps.STDOUT, stdout=sps.PIPE)
    proc3 = sps.Popen(cmd3, stderr=sps.STDOUT, stdout=sps.PIPE, stdin=proc1.stdout)

    ## wrap the actual call so we can kill it if anything goes awry
    while 1:
        try:
            if not isinstance(proc3.poll(), int):
                elapsed = datetime.timedelta(seconds=int(time.time()-start))
                done = len(glob.glob(os.path.join(tmpdir, 'chunk1_*')))
                progressbar(njobs, min(njobs, done), printstr.format(elapsed), spacer=data._spacer)
                time.sleep(0.1)
            else:
                res = proc3.communicate()[0]
                proc1.stdout.close()
                break

        except KeyboardInterrupt:
            proc1.kill()
            proc3.kill()
            raise KeyboardInterrupt()

    if proc3.returncode:
        raise IPyradWarningExit(" error in %s: %s", cmd3, res)

    ## grab output handles
    chunks1 = glob.glob(os.path.join(tmpdir, "chunk1_"+str(num)+"_*"))
    chunks1.sort()

    if "pair" in data.paramsdict["datatype"]:
        proc2 = sps.Popen(cmd2, stderr=sps.STDOUT, stdout=sps.PIPE)
        proc4 = sps.Popen(cmd4, stderr=sps.STDOUT, stdout=sps.PIPE, stdin=proc2.stdout)

        ## wrap the actual call so we can kill it if anything goes awry
        while 1:
            try:
                if not isinstance(proc4.poll(), int):
                    elapsed = datetime.timedelta(seconds=int(time.time()-start))
                    done = len(glob.glob(os.path.join(tmpdir, 'chunk1_*')))
                    progressbar(njobs, min(njobs, done), printstr.format(elapsed), data._spacer)
                    time.sleep(0.1)
                else:
                    res = proc4.communicate()[0]
                    proc2.stdout.close()
                    break

            except KeyboardInterrupt:
                proc2.kill()
                proc4.kill()
                raise KeyboardInterrupt()

        if proc4.returncode:
            raise IPyradWarningExit(" error in %s: %s", cmd4, res)

        ## grab output handles
        chunks2 = glob.glob(os.path.join(tmpdir, "chunk2_"+str(num)+"_*"))
        chunks2.sort()
    
    else:
        chunks2 = [0]*len(chunks1)

    assert len(chunks1) == len(chunks2), \
        "R1 and R2 files are not the same length."

    ## ensure full progress bar b/c estimates njobs could be off
    progressbar(10, 10, printstr.format(elapsed), spacer=data._spacer)
    return zip(chunks1, chunks2)