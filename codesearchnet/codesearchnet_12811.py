def index_reference_sequence(data, force=False):
    """ 
    Index the reference sequence, unless it already exists. Also make a mapping
    of scaffolds to index numbers for later user in steps 5-6. 
    """

    ## get ref file from params
    refseq_file = data.paramsdict['reference_sequence']
    index_files = []

    ## Check for existence of index files. Default to bwa unless you specify smalt
    if "smalt" in data._hackersonly["aligner"]:
        # These are smalt index files. Only referenced here to ensure they exist
        index_files.extend([".sma", ".smi"])
    else:
        index_files.extend([".amb", ".ann", ".bwt", ".pac", ".sa"])

    ## samtools specific index
    index_files.extend([".fai"])

    ## If reference sequence already exists then bail out of this func
    if not force:
        if all([os.path.isfile(refseq_file+i) for i in index_files]):
            return
    #if data._headers:
    #    print(INDEX_MSG.format(data._hackersonly["aligner"]))

    if "smalt" in data._hackersonly["aligner"]:
        ## Create smalt index for mapping
        ## smalt index [-k <wordlen>] [-s <stepsiz>]  <index_name> <reference_file>
        cmd1 = [ipyrad.bins.smalt, "index", 
                "-k", str(data._hackersonly["smalt_index_wordlen"]), 
                refseq_file, 
                refseq_file]
    else:
        ## bwa index <reference_file>
        cmd1 = [ipyrad.bins.bwa, "index", refseq_file]

    ## call the command
    LOGGER.info(" ".join(cmd1))
    proc1 = sps.Popen(cmd1, stderr=sps.STDOUT, stdout=sps.PIPE)
    error1 = proc1.communicate()[0]

    ## simple samtools index for grabbing ref seqs
    cmd2 = [ipyrad.bins.samtools, "faidx", refseq_file]
    LOGGER.info(" ".join(cmd2))
    proc2 = sps.Popen(cmd2, stderr=sps.STDOUT, stdout=sps.PIPE)
    error2 = proc2.communicate()[0]

    ## error handling
    if proc1.returncode:
        raise IPyradWarningExit(error1)
    if error2:
        if "please use bgzip" in error2:
            raise IPyradWarningExit(NO_ZIP_BINS.format(refseq_file))
        else:
            raise IPyradWarningExit(error2)