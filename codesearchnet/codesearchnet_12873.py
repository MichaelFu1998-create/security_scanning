def barmatch2(data, tups, cutters, longbar, matchdict, fnum):
    """
    cleaner barmatch func...
    """

    ## how many reads to store before writing to disk
    waitchunk = int(1e6)
    ## pid name for this engine
    epid = os.getpid()

    ## counters for total reads, those with cutsite, and those that matched
    filestat = np.zeros(3, dtype=np.int)
    ## store observed sample matches
    samplehits = {}
    ## dictionaries to store first and second reads until writing to file
    dsort1 = {} 
    dsort2 = {} 
    ## dictionary for all bars matched in sample
    dbars = {} 

    ## fill for sample names
    for sname in data.barcodes:
        if "-technical-replicate-" in sname:
            sname = sname.rsplit("-technical-replicate", 1)[0]
        samplehits[sname] = 0
        dsort1[sname] = []
        dsort2[sname] = []
        dbars[sname] = set()

    ## store observed bars
    barhits = {}
    for barc in matchdict:
        barhits[barc] = 0

    ## store others
    misses = {}
    misses['_'] = 0

    ## build func for finding barcode
    getbarcode = get_barcode_func(data, longbar)

    ## get quart iterator of reads
    if tups[0].endswith(".gz"):
        ofunc = gzip.open
    else:
        ofunc = open

    ## create iterators 
    ofile1 = ofunc(tups[0], 'r')
    fr1 = iter(ofile1) 
    quart1 = itertools.izip(fr1, fr1, fr1, fr1)
    if tups[1]:
        ofile2 = ofunc(tups[1], 'r')
        fr2 = iter(ofile2)  
        quart2 = itertools.izip(fr2, fr2, fr2, fr2)
        quarts = itertools.izip(quart1, quart2)
    else:
        quarts = itertools.izip(quart1, iter(int, 1))

    ## go until end of the file
    while 1:
        try:
            read1, read2 = quarts.next()
            read1 = list(read1)
            filestat[0] += 1
        except StopIteration:
            break
    
        barcode = ""
        ## Get barcode_R2 and check for matching sample name
        if '3rad' in data.paramsdict["datatype"]:
            ## Here we're just reusing the findbcode function
            ## for R2, and reconfiguring the longbar tuple to have the
            ## maxlen for the R2 barcode
            ## Parse barcode. Use the parsing function selected above.
            barcode1 = find3radbcode(cutters=cutters, 
                                longbar=longbar, read1=read1)
            barcode2 = find3radbcode(cutters=cutters, 
                                longbar=(longbar[2], longbar[1]), read1=read2)
            barcode = barcode1 + "+" + barcode2
        else:
            ## Parse barcode. Uses the parsing function selected above.
            barcode = getbarcode(cutters, read1, longbar)
   
        ## find if it matches 
        sname_match = matchdict.get(barcode)

        if sname_match:
            #sample_index[filestat[0]-1] = snames.index(sname_match) + 1
            ## record who matched
            dbars[sname_match].add(barcode)
            filestat[1] += 1
            filestat[2] += 1
            samplehits[sname_match] += 1
            barhits[barcode] += 1
            if barcode in barhits:
                barhits[barcode] += 1
            else:
                barhits[barcode] = 1
    
            ## trim off barcode
            lenbar = len(barcode)
            if '3rad' in data.paramsdict["datatype"]:
                ## Iff 3rad trim the len of the first barcode
                lenbar = len(barcode1)
    
            if data.paramsdict["datatype"] == '2brad':
                overlen = len(cutters[0][0]) + lenbar + 1
                read1[1] = read1[1][:-overlen] + "\n"
                read1[3] = read1[3][:-overlen] + "\n"
            else:
                read1[1] = read1[1][lenbar:]
                read1[3] = read1[3][lenbar:]
    
            ## Trim barcode off R2 and append. Only 3rad datatype
            ## pays the cpu cost of splitting R2
            if '3rad' in data.paramsdict["datatype"]:
                read2 = list(read2)
                read2[1] = read2[1][len(barcode2):]
                read2[3] = read2[3][len(barcode2):]
    
            ## append to dsort
            dsort1[sname_match].append("".join(read1))
            if 'pair' in data.paramsdict["datatype"]:
                dsort2[sname_match].append("".join(read2))

        else:
            misses["_"] += 1
            if barcode:
                filestat[1] += 1

        ## how can we make it so all of the engines aren't trying to write to
        ## ~100-200 files all at the same time? This is the I/O limit we hit..
        ## write out at 100K to keep memory low. It is fine on HPC which can 
        ## write parallel, but regular systems might crash
        if not filestat[0] % waitchunk:
            ## write the remaining reads to file"
            writetofile(data, dsort1, 1, epid)
            if 'pair' in data.paramsdict["datatype"]:
                writetofile(data, dsort2, 2, epid)
            ## clear out dsorts
            for sample in data.barcodes:
                if "-technical-replicate-" in sname:
                    sname = sname.rsplit("-technical-replicate", 1)[0]
                dsort1[sname] = []
                dsort2[sname] = []
            ## reset longlist
            #longlist = np.zeros(waitchunk, dtype=np.uint32)                

    ## close open files
    ofile1.close()
    if tups[1]:
        ofile2.close()

    ## write the remaining reads to file
    writetofile(data, dsort1, 1, epid)
    if 'pair' in data.paramsdict["datatype"]:
        writetofile(data, dsort2, 2, epid)

    ## return stats in saved pickle b/c return_queue is too small
    ## and the size of the match dictionary can become quite large
    samplestats = [samplehits, barhits, misses, dbars]
    outname = os.path.join(data.dirs.fastqs, "tmp_{}_{}.p".format(epid, fnum))
    with open(outname, 'w') as wout:
        pickle.dump([filestat, samplestats], wout)

    return outname