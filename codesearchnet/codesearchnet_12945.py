def concat_reads(data, subsamples, ipyclient):
    """ concatenate if multiple input files for a single samples """

    ## concatenate reads if they come from merged assemblies.
    if any([len(i.files.fastqs) > 1 for i in subsamples]):
        ## run on single engine for now
        start = time.time()
        printstr = " concatenating inputs  | {} | s2 |"
        finished = 0
        catjobs = {}
        for sample in subsamples:
            if len(sample.files.fastqs) > 1:
                catjobs[sample.name] = ipyclient[0].apply(\
                                       concat_multiple_inputs, *(data, sample))
            else:
                sample.files.concat = sample.files.fastqs

        ## wait for all to finish
        while 1:
            finished = sum([i.ready() for i in catjobs.values()])
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            progressbar(len(catjobs), finished, printstr.format(elapsed), spacer=data._spacer)
            time.sleep(0.1)
            if finished == len(catjobs):
                print("")
                break

        ## collect results, which are concat file handles.
        for async in catjobs:
            if catjobs[async].successful():
                data.samples[async].files.concat = catjobs[async].result()
            else:
                error = catjobs[async].result()#exception()
                LOGGER.error("error in step2 concat %s", error)
                raise IPyradWarningExit("error in step2 concat: {}".format(error))
    else:
        for sample in subsamples:
            ## just copy fastqs handles to concat attribute
            sample.files.concat = sample.files.fastqs

    return subsamples