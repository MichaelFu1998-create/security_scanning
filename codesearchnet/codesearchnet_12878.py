def prechecks2(data, force):
    """
    A new simplified version of prechecks func before demux
    Checks before starting analysis. 
    -----------------------------------
    1) Is there data in raw_fastq_path
    2) Is there a barcode file
    3) Is there a workdir and fastqdir
    4) remove old fastq/tmp_sample_R*_ dirs/
    5) return file names as pairs (r1, r2) or fakepairs (r1, 1)
    6) get ambiguous cutter resolutions
    7) get optim size
    """

    ## check for data using glob for fuzzy matching
    if not glob.glob(data.paramsdict["raw_fastq_path"]):
        raise IPyradWarningExit(NO_RAWS.format(data.paramsdict["raw_fastq_path"]))

    ## find longest barcode
    try:
        ## Handle 3rad multi-barcodes. Gets len of the first one. 
        ## Should be harmless for single barcode data
        barlens = [len(i.split("+")[0]) for i in data.barcodes.values()]
        if len(set(barlens)) == 1:
            longbar = (barlens[0], 'same')
        else:
            longbar = (max(barlens), 'diff')

        ## For 3rad we need to add the length info for barcodes_R2
        if "3rad" in data.paramsdict["datatype"]:
            barlens = [len(i.split("+")[1]) for i in data.barcodes.values()]
            longbar = (longbar[0], longbar[1], max(barlens))
    except ValueError:
        raise IPyradWarningExit(NO_BARS.format(data.paramsdict["barcodes_path"]))

    ## setup dirs: [workdir] and a [workdir/name_fastqs]
    opj = os.path.join

    ## create project dir
    pdir = os.path.realpath(data.paramsdict["project_dir"])
    if not os.path.exists(pdir):
        os.mkdir(pdir)

    ## create fastq dir
    data.dirs.fastqs = opj(pdir, data.name+"_fastqs")
    if os.path.exists(data.dirs.fastqs) and force:
        print(OVERWRITING_FASTQS.format(**{"spacer":data._spacer}))
        shutil.rmtree(data.dirs.fastqs)
    if not os.path.exists(data.dirs.fastqs):
        os.mkdir(data.dirs.fastqs)

    ## insure no leftover tmp files from a previous run (there shouldn't be)
    oldtmps = glob.glob(os.path.join(data.dirs.fastqs, "tmp_*_R1_"))
    oldtmps += glob.glob(os.path.join(data.dirs.fastqs, "tmp_*_R2_"))    
    for oldtmp in oldtmps:
        os.remove(oldtmp)

    ## gather raw sequence filenames (people want this to be flexible ...)
    if 'pair' in data.paramsdict["datatype"]:
        raws = combinefiles(data.paramsdict["raw_fastq_path"])
    else:
        raws = zip(glob.glob(data.paramsdict["raw_fastq_path"]), iter(int, 1))

    ## returns a list of both resolutions of cut site 1
    ## (TGCAG, ) ==> [TGCAG, ]
    ## (TWGC, ) ==> [TAGC, TTGC]
    ## (TWGC, AATT) ==> [TAGC, TTGC]
    cutters = [ambigcutters(i) for i in data.paramsdict["restriction_overhang"]]
    print(cutters)
    assert cutters, "Must enter a `restriction_overhang` for demultiplexing."

    ## get matchdict
    matchdict = inverse_barcodes(data)

    ## return all
    return raws, longbar, cutters, matchdict