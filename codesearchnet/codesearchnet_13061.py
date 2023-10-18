def make_chunks(data, samples, lbview):
    """
    calls chunk_clusters and tracks progress.
    """
    ## first progress bar
    start = time.time()
    printstr = " chunking clusters     | {} | s5 |"
    elapsed = datetime.timedelta(seconds=int(time.time()-start))
    progressbar(10, 0, printstr.format(elapsed), spacer=data._spacer)

    ## send off samples to be chunked
    lasyncs = {}
    for sample in samples:
        lasyncs[sample.name] = lbview.apply(chunk_clusters, *(data, sample))

    ## block until finished
    while 1:
        ready = [i.ready() for i in lasyncs.values()]
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(len(ready), sum(ready), printstr.format(elapsed), spacer=data._spacer)
        time.sleep(0.1)
        if len(ready) == sum(ready):
            print("")
            break

    ## check for failures
    for sample in samples:
        if not lasyncs[sample.name].successful():
            LOGGER.error("  sample %s failed: %s", sample.name, 
                        lasyncs[sample.name].exception())

    return lasyncs