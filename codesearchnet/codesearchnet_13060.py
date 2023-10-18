def calculate_depths(data, samples, lbview):
    """
    check whether mindepth has changed, and thus whether clusters_hidepth
    needs to be recalculated, and get new maxlen for new highdepth clusts.
    if mindepth not changed then nothing changes.
    """

    ## send jobs to be processed on engines
    start = time.time()
    printstr = " calculating depths    | {} | s5 |"
    recaljobs = {}
    maxlens = []
    for sample in samples:
        recaljobs[sample.name] = lbview.apply(recal_hidepth, *(data, sample))

    ## block until finished
    while 1:
        ready = [i.ready() for i in recaljobs.values()]
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(len(ready), sum(ready), printstr.format(elapsed), spacer=data._spacer)
        time.sleep(0.1)
        if len(ready) == sum(ready):
            print("")
            break

    ## check for failures and collect results
    modsamples = []
    for sample in samples:
        if not recaljobs[sample.name].successful():
            LOGGER.error("  sample %s failed: %s", sample.name, recaljobs[sample.name].exception())
        else:
            modsample, _, maxlen, _, _ = recaljobs[sample.name].result()
            modsamples.append(modsample)
            maxlens.append(maxlen)

    ## reset global maxlen if something changed
    data._hackersonly["max_fragment_length"] = int(max(maxlens)) + 4

    return samples