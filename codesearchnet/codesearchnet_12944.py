def run2(data, samples, force, ipyclient):
    """ 
    Filter for samples that are already finished with this step, allow others
    to run, pass them to parallel client function to filter with cutadapt. 
    """

    ## create output directories 
    data.dirs.edits = os.path.join(os.path.realpath(
                                   data.paramsdict["project_dir"]), 
                                   data.name+"_edits")
    if not os.path.exists(data.dirs.edits):
        os.makedirs(data.dirs.edits)

    ## get samples
    subsamples = choose_samples(samples, force)

    ## only allow extra adapters in filters==3, 
    ## and add poly repeats if not in list of adapters
    if int(data.paramsdict["filter_adapters"]) == 3:
        if not data._hackersonly["p3_adapters_extra"]:
            for poly in ["A"*8, "T"*8, "C"*8, "G"*8]:
                data._hackersonly["p3_adapters_extra"].append(poly)
        if not data._hackersonly["p5_adapters_extra"]:    
            for poly in ["A"*8, "T"*8, "C"*8, "G"*8]:
                data._hackersonly["p5_adapters_extra"].append(poly)
    else:
        data._hackersonly["p5_adapters_extra"] = []
        data._hackersonly["p3_adapters_extra"] = []

    ## concat is not parallelized (since it's disk limited, generally)
    subsamples = concat_reads(data, subsamples, ipyclient)

    ## cutadapt is parallelized by ncores/2 because cutadapt spawns threads
    lbview = ipyclient.load_balanced_view(targets=ipyclient.ids[::2])
    run_cutadapt(data, subsamples, lbview)

    ## cleanup is ...
    assembly_cleanup(data)