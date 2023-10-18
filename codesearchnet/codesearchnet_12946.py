def run_cutadapt(data, subsamples, lbview):
    """
    sends fastq files to cutadapt
    """
    ## choose cutadapt function based on datatype
    start = time.time()
    printstr = " processing reads      | {} | s2 |"
    finished = 0
    rawedits = {}

    ## sort subsamples so that the biggest files get submitted first
    subsamples.sort(key=lambda x: x.stats.reads_raw, reverse=True)
    LOGGER.info([i.stats.reads_raw for i in subsamples])

    ## send samples to cutadapt filtering
    if "pair" in data.paramsdict["datatype"]:
        for sample in subsamples:
            rawedits[sample.name] = lbview.apply(cutadaptit_pairs, *(data, sample))
    else:
        for sample in subsamples:
            rawedits[sample.name] = lbview.apply(cutadaptit_single, *(data, sample))

    ## wait for all to finish
    while 1:
        finished = sum([i.ready() for i in rawedits.values()])
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        progressbar(len(rawedits), finished, printstr.format(elapsed), spacer=data._spacer)
        time.sleep(0.1)
        if finished == len(rawedits):
            print("")
            break

    ## collect results, report failures, and store stats. async = sample.name
    for async in rawedits:
        if rawedits[async].successful():
            res = rawedits[async].result()

            ## if single cleanup is easy
            if "pair" not in data.paramsdict["datatype"]:
                parse_single_results(data, data.samples[async], res)
            else:
                parse_pair_results(data, data.samples[async], res)
        else:
            print("  found an error in step2; see ipyrad_log.txt")
            LOGGER.error("error in run_cutadapt(): %s", rawedits[async].exception())