def cutadaptit_single(data, sample):
    """ 
    Applies quality and adapter filters to reads using cutadapt. If the ipyrad
    filter param is set to 0 then it only filters to hard trim edges and uses
    mintrimlen. If filter=1, we add quality filters. If filter=2 we add
    adapter filters. 
    """

    sname = sample.name
    ## if (GBS, ddRAD) we look for the second cut site + adapter. For single-end
    ## data we don't bother trying to remove the second barcode since it's not
    ## as critical as with PE data.
    if data.paramsdict["datatype"] == "rad":
        adapter = data._hackersonly["p3_adapter"]
    else:
        ## if GBS then the barcode can also be on the other side. 
        if data.paramsdict["datatype"] == "gbs":

            ## make full adapter (-revcompcut-revcompbarcode-adapter)
            ## and add adapter without revcompbarcode
            if data.barcodes:
                adapter = \
                    fullcomp(data.paramsdict["restriction_overhang"][1])[::-1] \
                  + fullcomp(data.barcodes[sample.name])[::-1] \
                  + data._hackersonly["p3_adapter"]
                ## add incomplete adapter to extras (-recompcut-adapter)
                data._hackersonly["p3_adapters_extra"].append(
                    fullcomp(data.paramsdict["restriction_overhang"][1])[::-1] \
                  + data._hackersonly["p3_adapter"])
            else:
                LOGGER.warning("No barcode information present, and is therefore not "+\
                               "being used for adapter trimming of SE gbs data.")
                ## else no search for barcodes on 3'
                adapter = \
                    fullcomp(data.paramsdict["restriction_overhang"][1])[::-1] \
                  + data._hackersonly["p3_adapter"]
        else:
            adapter = \
                fullcomp(data.paramsdict["restriction_overhang"][1])[::-1] \
              + data._hackersonly["p3_adapter"]

    ## get length trim parameter from new or older version of ipyrad params
    trim5r1 = trim3r1 = []
    if data.paramsdict.get("trim_reads"):
        trimlen = data.paramsdict.get("trim_reads")
        
        ## trim 5' end
        if trimlen[0]:
            trim5r1 = ["-u", str(trimlen[0])]
        if trimlen[1] < 0:
            trim3r1 = ["-u", str(trimlen[1])]
        if trimlen[1] > 0:
            trim3r1 = ["--length", str(trimlen[1])]
    else:
        trimlen = data.paramsdict.get("edit_cutsites")
        trim5r1 = ["--cut", str(trimlen[0])]

    ## testing new 'trim_reads' setting
    cmdf1 = ["cutadapt"]
    if trim5r1:
        cmdf1 += trim5r1
    if trim3r1:
        cmdf1 += trim3r1
    cmdf1 += ["--minimum-length", str(data.paramsdict["filter_min_trim_len"]),
              "--max-n", str(data.paramsdict["max_low_qual_bases"]),
              "--trim-n", 
              "--output", OPJ(data.dirs.edits, sname+".trimmed_R1_.fastq.gz"),
              sample.files.concat[0][0]]

    if int(data.paramsdict["filter_adapters"]):
        ## NEW: only quality trim the 3' end for SE data.
        cmdf1.insert(1, "20")
        cmdf1.insert(1, "-q")
        cmdf1.insert(1, str(data.paramsdict["phred_Qscore_offset"]))
        cmdf1.insert(1, "--quality-base")

    ## if filter_adapters==3 then p3_adapters_extra will already have extra
    ## poly adapters added to its list. 
    if int(data.paramsdict["filter_adapters"]) > 1:
        ## first enter extra cuts (order of input is reversed)
        for extracut in list(set(data._hackersonly["p3_adapters_extra"]))[::-1]:
            cmdf1.insert(1, extracut)
            cmdf1.insert(1, "-a")
        ## then put the main cut so it appears first in command
        cmdf1.insert(1, adapter)
        cmdf1.insert(1, "-a")


    ## do modifications to read1 and write to tmp file
    LOGGER.info(cmdf1)
    proc1 = sps.Popen(cmdf1, stderr=sps.STDOUT, stdout=sps.PIPE, close_fds=True)
    try:
        res1 = proc1.communicate()[0]
    except KeyboardInterrupt:
        proc1.kill()
        raise KeyboardInterrupt

    ## raise errors if found
    if proc1.returncode:
        raise IPyradWarningExit(" error in {}\n {}".format(" ".join(cmdf1), res1))

    ## return result string to be parsed outside of engine
    return res1