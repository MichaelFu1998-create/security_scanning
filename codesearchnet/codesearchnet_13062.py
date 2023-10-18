def process_chunks(data, samples, lasyncs, lbview):
    """
    submit chunks to consens func and ...
    """

    ## send chunks to be processed
    start = time.time()
    asyncs = {sample.name:[] for sample in samples}
    printstr = " consens calling       | {} | s5 |"

    ## get chunklist from results
    for sample in samples:
        clist = lasyncs[sample.name].result()
        for optim, chunkhandle in clist:
            args = (data, sample, chunkhandle, optim)
            #asyncs[sample.name].append(lbview.apply_async(consensus, *args))
            asyncs[sample.name].append(lbview.apply_async(newconsensus, *args))
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            progressbar(10, 0, printstr.format(elapsed), spacer=data._spacer)

    ## track progress
    allsyncs = list(itertools.chain(*[asyncs[i.name] for i in samples]))
    while 1:
        ready = [i.ready() for i in allsyncs]
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(len(ready), sum(ready), printstr.format(elapsed), spacer=data._spacer)
        time.sleep(0.1)
        if len(ready) == sum(ready):
            break

    ## get clean samples
    casyncs = {}
    for sample in samples:
        rlist = asyncs[sample.name]
        statsdicts = [i.result() for i in rlist]
        casyncs[sample.name] = lbview.apply(cleanup, *(data, sample, statsdicts))
    while 1:
        ready = [i.ready() for i in casyncs.values()]
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(10, 10, printstr.format(elapsed), spacer=data._spacer)
        time.sleep(0.1)
        if len(ready) == sum(ready):
            print("")
            break

    ## check for failures:
    for key in asyncs:
        asynclist = asyncs[key]
        for async in asynclist:
            if not async.successful():
                LOGGER.error("  async error: %s \n%s", key, async.exception())
    for key in casyncs:
        if not casyncs[key].successful():
            LOGGER.error("  casync error: %s \n%s", key, casyncs[key].exception())

    ## get samples back
    subsamples = [i.result() for i in casyncs.values()]
    for sample in subsamples:
        data.samples[sample.name] = sample

    ## build Assembly stats
    data.stats_dfs.s5 = data._build_stat("s5")

    ## write stats file
    data.stats_files.s5 = os.path.join(data.dirs.consens, 's5_consens_stats.txt')
    with io.open(data.stats_files.s5, 'w') as out:
        #out.write(data.stats_dfs.s5.to_string())
        data.stats_dfs.s5.to_string(
            buf=out,
            formatters={
                'clusters_total':'{:.0f}'.format,
                'filtered_by_depth':'{:.0f}'.format,
                'filtered_by_maxH':'{:.0f}'.format,
                'filtered_by_maxN':'{:.0f}'.format,
                'reads_consens':'{:.0f}'.format,
                'nsites':'{:.0f}'.format,
                'nhetero':'{:.0f}'.format,
                'heterozygosity':'{:.5f}'.format
            })