def cutadaptit_pairs(data, sample):
    """
    Applies trim & filters to pairs, including adapter detection. If we have
    barcode information then we use it to trim reversecut+bcode+adapter from 
    reverse read, if not then we have to apply a more general cut to make sure 
    we remove the barcode, this uses wildcards and so will have more false 
    positives that trim a little extra from the ends of reads. Should we add
    a warning about this when filter_adapters=2 and no barcodes?
    """
    LOGGER.debug("Entering cutadaptit_pairs - {}".format(sample.name))
    sname = sample.name

    ## applied to read pairs
    #trim_r1 = str(data.paramsdict["edit_cutsites"][0])
    #trim_r2 = str(data.paramsdict["edit_cutsites"][1])
    finput_r1 = sample.files.concat[0][0]
    finput_r2 = sample.files.concat[0][1]

    ## Get adapter sequences. This is very important. For the forward adapter
    ## we don't care all that much about getting the sequence just before the 
    ## Illumina adapter, b/c it will either be random (in RAD), or the reverse
    ## cut site of cut1 or cut2 (gbs or ddrad). Either way, we can still trim it 
    ## off later in step7 with trim overhang if we want. And it should be invar-
    ## iable unless the cut site has an ambiguous char. The reverse adapter is 
    ## super important, however b/c it can contain the inline barcode and 
    ## revcomp cut site. We def want to trim out the barcode, and ideally the 
    ## cut site too to be safe. Problem is we don't always know the barcode if 
    ## users demultiplexed their data elsewhere. So, if barcode is missing we 
    ## do a very fuzzy match before the adapter and trim it out. 

    ## this just got more complicated now that we allow merging technical
    ## replicates in step 1 since a single sample might have multiple barcodes
    ## associated with it and so we need to search for multiple adapter+barcode
    ## combinations.
    ## We will assume that if they are 'linking_barcodes()' here then there are
    ## no technical replicates in the barcodes file. If there ARE technical
    ## replicates, then they should run step1 so they are merged, in which case
    ## the sample specific barcodes will be saved to each Sample under its
    ## .barcode attribute as a list. 

    if not data.barcodes:
        ## try linking barcodes again in case user just added a barcodes path
        ## after receiving the warning. We assume no technical replicates here.
        try:
            data._link_barcodes()
        except Exception as inst:
            LOGGER.warning("  error adding barcodes info: %s", inst)

    ## barcodes are present meaning they were parsed to the samples in step 1.
    if data.barcodes:
        try:
            adapter1 = fullcomp(data.paramsdict["restriction_overhang"][1])[::-1] \
                        + data._hackersonly["p3_adapter"]
            if isinstance(sample.barcode, list):
                bcode = fullcomp(sample.barcode[0])[::-1]
            elif isinstance(data.barcodes[sample.name], list):
                bcode = fullcomp(data.barcodes[sample.name][0][::-1])
            else:
                bcode = fullcomp(data.barcodes[sample.name])[::-1]
            ## add full adapter (-revcompcut-revcompbcode-adapter)
            adapter2 = fullcomp(data.paramsdict["restriction_overhang"][0])[::-1] \
                        + bcode \
                        + data._hackersonly["p5_adapter"]      
        except KeyError as inst:
            msg = """
    Sample name does not exist in the barcode file. The name in the barcode file
    for each sample must exactly equal the raw file name for the sample minus
    `_R1`. So for example a sample called WatDo_PipPrep_R1_100.fq.gz must
    be referenced in the barcode file as WatDo_PipPrep_100. The name in your
    barcode file for this sample must match: {}
    """.format(sample.name)
            LOGGER.error(msg)
            raise IPyradWarningExit(msg)
    else:
        print(NO_BARS_GBS_WARNING)
        #adapter1 = fullcomp(data.paramsdict["restriction_overhang"][1])[::-1]+\
        #           data._hackersonly["p3_adapter"]
        #adapter2 = "XXX"
        adapter1 = data._hackersonly["p3_adapter"]
        adapter2 = fullcomp(data._hackersonly["p5_adapter"])


    ## parse trim_reads
    trim5r1 = trim5r2 = trim3r1 = trim3r2 = []
    if data.paramsdict.get("trim_reads"):
        trimlen = data.paramsdict.get("trim_reads")
        
        ## trim 5' end
        if trimlen[0]:
            trim5r1 = ["-u", str(trimlen[0])]
        if trimlen[1] < 0:
            trim3r1 = ["-u", str(trimlen[1])]
        if trimlen[1] > 0:
            trim3r1 = ["--length", str(trimlen[1])]

        ## legacy support for trimlen = 0,0 default
        if len(trimlen) > 2:
            if trimlen[2]:
                trim5r2 = ["-U", str(trimlen[2])]

        if len(trimlen) > 3:
            if trimlen[3]:
                if trimlen[3] < 0:
                    trim3r2 = ["-U", str(trimlen[3])]
                if trimlen[3] > 0:            
                    trim3r2 = ["--length", str(trimlen[3])]

    else:
        ## legacy support
        trimlen = data.paramsdict.get("edit_cutsites")
        trim5r1 = ["-u", str(trimlen[0])]
        trim5r2 = ["-U", str(trimlen[1])]

    ## testing new 'trim_reads' setting
    cmdf1 = ["cutadapt"]
    if trim5r1:
        cmdf1 += trim5r1
    if trim3r1:
        cmdf1 += trim3r1
    if trim5r2:
        cmdf1 += trim5r2
    if trim3r2:
        cmdf1 += trim3r2

    cmdf1 += ["--trim-n",
              "--max-n", str(data.paramsdict["max_low_qual_bases"]),
              "--minimum-length", str(data.paramsdict["filter_min_trim_len"]),
              "-o", OPJ(data.dirs.edits, sname+".trimmed_R1_.fastq.gz"),
              "-p", OPJ(data.dirs.edits, sname+".trimmed_R2_.fastq.gz"),
              finput_r1,
              finput_r2]

    ## additional args
    if int(data.paramsdict["filter_adapters"]) < 2:
        ## add a dummy adapter to let cutadapt know whe are not using legacy-mode
        cmdf1.insert(1, "XXX")
        cmdf1.insert(1, "-A")

    if int(data.paramsdict["filter_adapters"]):
        cmdf1.insert(1, "20,20")
        cmdf1.insert(1, "-q")
        cmdf1.insert(1, str(data.paramsdict["phred_Qscore_offset"]))
        cmdf1.insert(1, "--quality-base")

    if int(data.paramsdict["filter_adapters"]) > 1:
        ## if technical replicates then add other copies
        if isinstance(sample.barcode, list):
            for extrabar in sample.barcode[1:]:
                data._hackersonly["p5_adapters_extra"] += \
                    fullcomp(data.paramsdict["restriction_overhang"][0])[::-1] + \
                    fullcomp(extrabar)[::-1] + \
                    data._hackersonly["p5_adapter"]
                data._hackersonly["p5_adapters_extra"] += \
                    fullcomp(data.paramsdict["restriction_overhang"][1])[::-1] + \
                    data._hackersonly["p3_adapter"]

        ## first enter extra cuts
        zcut1 = list(set(data._hackersonly["p3_adapters_extra"]))[::-1]
        zcut2 = list(set(data._hackersonly["p5_adapters_extra"]))[::-1]
        for ecut1, ecut2 in zip(zcut1, zcut2):
            cmdf1.insert(1, ecut1)
            cmdf1.insert(1, "-a")
            cmdf1.insert(1, ecut2)
            cmdf1.insert(1, "-A")
        ## then put the main cut first
        cmdf1.insert(1, adapter1)
        cmdf1.insert(1, '-a')        
        cmdf1.insert(1, adapter2)
        cmdf1.insert(1, '-A')         

    ## do modifications to read1 and write to tmp file
    LOGGER.debug(" ".join(cmdf1))
    #sys.exit()
    try:
        proc1 = sps.Popen(cmdf1, stderr=sps.STDOUT, stdout=sps.PIPE, close_fds=True)
        res1 = proc1.communicate()[0]
    except KeyboardInterrupt:
        proc1.kill()
        LOGGER.info("this is where I want it to interrupt")
        raise KeyboardInterrupt()

    ## raise errors if found
    if proc1.returncode:
        raise IPyradWarningExit(" error [returncode={}]: {}\n{}"\
            .format(proc1.returncode, " ".join(cmdf1), res1))

    LOGGER.debug("Exiting cutadaptit_pairs - {}".format(sname))
    ## return results string to be parsed outside of engine
    return res1