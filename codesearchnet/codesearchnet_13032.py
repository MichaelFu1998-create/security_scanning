def trackjobs(func, results, spacer):
    """
    Blocks and prints progress for just the func being requested from a list
    of submitted engine jobs. Returns whether any of the jobs failed.

    func = str
    results = dict of asyncs
    """

    ## TODO: try to insert a better way to break on KBD here.
    LOGGER.info("inside trackjobs of %s", func)

    ## get just the jobs from results that are relevant to this func
    asyncs = [(i, results[i]) for i in results if i.split("-", 2)[0] == func]

    ## progress bar
    start = time.time()
    while 1:
        ## how many of this func have finished so far
        ready = [i[1].ready() for i in asyncs]
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        printstr = " {}    | {} | s3 |".format(PRINTSTR[func], elapsed)
        progressbar(len(ready), sum(ready), printstr, spacer=spacer)
        time.sleep(0.1)
        if len(ready) == sum(ready):
            print("")
            break

    sfails = []
    errmsgs = []
    for job in asyncs:
        if not job[1].successful():
            sfails.append(job[0])
            errmsgs.append(job[1].result())

    return func, sfails, errmsgs