def _paramschecker(self, param, newvalue):
    """ Raises exceptions when params are set to values they should not be"""

    if param == 'assembly_name':
        ## Make sure somebody doesn't try to change their assembly_name, bad
        ## things would happen. Calling set_params on assembly_name only raises
        ## an informative error. Assembly_name is set at Assembly creation time
        ## and is immutable.
        raise IPyradWarningExit(CANNOT_CHANGE_ASSEMBLY_NAME)

    elif param == 'project_dir':
        expandpath = _expander(newvalue)
        if not expandpath.startswith("/"):
            if os.path.exists(expandpath):
                expandpath = _expander(expandpath)
        ## Forbid spaces in path names
        if " " in expandpath:
            raise IPyradWarningExit(BAD_PROJDIR_NAME.format(expandpath))
        self.paramsdict["project_dir"] = expandpath
        self.dirs["project"] = expandpath

    ## `Merged:` in newvalue for raw_fastq_path indicates that this
    ## assembly is a merge of several others, so this param has no
    ## value for this assembly
    elif param == 'raw_fastq_path':
        if newvalue and not "Merged:" in newvalue:
            fullrawpath = _expander(newvalue)
            if os.path.isdir(fullrawpath):
                raise IPyradWarningExit(RAW_PATH_ISDIR.format(fullrawpath))
            ## if something is found in path
            elif glob.glob(fullrawpath):
                self.paramsdict['raw_fastq_path'] = fullrawpath
            ## else allow empty, tho it can still raise an error in step1
            else:
                raise IPyradWarningExit(NO_RAW_FILE.format(fullrawpath))
        else:
            self.paramsdict['raw_fastq_path'] = ""


    ## `Merged:` in newvalue for barcodes_path indicates that this
    ## assembly is a merge of several others, so this param has no
    ## value for this assembly
    elif param == 'barcodes_path':
        ## if a value was entered check that it exists
        if newvalue and not "Merged:" in newvalue:
            ## also allow for fuzzy match in names using glob
            fullbarpath = glob.glob(_expander(newvalue))[0]
            ## raise error if file is not found
            if not os.path.exists(fullbarpath):
                raise IPyradWarningExit(BARCODE_NOT_FOUND.format(fullbarpath))
            else:
                self.paramsdict['barcodes_path'] = fullbarpath
                self._link_barcodes()

        ## if no path was entered then set barcodes path to empty.
        ## this is checked again during step 1 and will raise an error
        ## if you try demultiplexing without a barcodes file
        else:
            self.paramsdict['barcodes_path'] = newvalue


    ## `Merged:` in newvalue for sorted_fastq_path indicates that this
    ## assembly is a merge of several others, so this param has no
    ## value for this assembly
    elif param == 'sorted_fastq_path':
        if newvalue and not "Merged:" in newvalue:
            fullsortedpath = _expander(newvalue)

            if os.path.isdir(fullsortedpath):
                raise IPyradWarningExit(SORTED_ISDIR.format(fullsortedpath))
            elif glob.glob(fullsortedpath):
                self.paramsdict['sorted_fastq_path'] = fullsortedpath

            else:
                raise IPyradWarningExit(SORTED_NOT_FOUND.format(fullsortedpath))
        ## if no value was entered then set to "".
        else:
            self.paramsdict['sorted_fastq_path'] = ""


    elif param == 'assembly_method':
        ## TEMPORARY BLOCK ON DENOVO+REFERENCE METHOD
#        if newvalue == "denovo+reference":
#            raise IPyradWarningExit("""
#    Error: The 'denovo+reference' method is temporarily blocked while we 
#    refactor it to greatly improve the speed. You can either revert to an
#    older version (pre v.0.7.0) or wait for the next update to resume using
#    this method. 
#    """)

        methods = ["denovo", "reference", "denovo+reference", "denovo-reference"]
        assert newvalue in methods, BAD_ASSEMBLY_METHOD.format(newvalue)
        self.paramsdict['assembly_method'] = newvalue


    elif param == 'reference_sequence':
        if newvalue:
            fullrawpath = _expander(newvalue)
            if not os.path.isfile(fullrawpath):
                LOGGER.info("reference sequence file not found.")
                raise IPyradWarningExit(REF_NOT_FOUND.format(fullrawpath))
            self.paramsdict['reference_sequence'] = fullrawpath
        ## if no value was entered the set to "". Will be checked again
        ## at step3 if user tries to do refseq and raise error
        else:
            self.paramsdict['reference_sequence'] = ""


    elif param == 'datatype':
        ## list of allowed datatypes
        datatypes = ['rad', 'gbs', 'ddrad', 'pairddrad',
                     'pairgbs', 'merged', '2brad', 'pair3rad']
        ## raise error if something else
        if str(newvalue) not in datatypes:
            raise IPyradError("""
    datatype {} not recognized, must be one of: {}
    """.format(newvalue, datatypes))
        else:
            self.paramsdict['datatype'] = str(newvalue)
            ## link_barcodes is called before datatypes is set
            ## we need to know the datatype so we can read in
            ## the multiplexed barcodes for 3rad. This seems
            ## a little annoying, but it was better than any
            ## alternatives I could think of.
            if "3rad" in self.paramsdict['datatype'] and not \
            self.paramsdict['sorted_fastq_path'].strip():
                if not "Merged:" in self.paramsdict['barcodes_path']:
                    self._link_barcodes()

    elif param == 'restriction_overhang':
        newvalue = _tuplecheck(newvalue, str)
        assert isinstance(newvalue, tuple), """
    cut site must be a tuple, e.g., (TGCAG, '') or (TGCAG, CCGG)"""
        ## Handle the special case where the user has 1
        ## restriction overhang and does not include the trailing comma
        if len(newvalue) == 1:
            ## for gbs users might not know to enter the second cut site
            ## so we do it for them.
            if self.paramsdict["datatype"] == "gbs":
                newvalue += newvalue
            else:
                newvalue += ("",)
        #=======
        #    newvalue = (newvalue[0], "")
        #>>>>>>> d40a5d5086a0d0aace04dd08338ec4ba5341d1f2

        ## Handle 3rad datatype with only 3 cutters
        if len(newvalue) == 3:
            newvalue = (newvalue[0], newvalue[1], newvalue[2], "")
        assert len(newvalue) <= 4, """
    most datasets require 1 or 2 cut sites, e.g., (TGCAG, '') or (TGCAG, CCGG).
    For 3rad/seqcap may be up to 4 cut sites."""
        self.paramsdict['restriction_overhang'] = newvalue

    elif param == 'max_low_qual_bases':
        assert isinstance(int(newvalue), int), """
    max_low_qual_bases must be an integer."""
        self.paramsdict['max_low_qual_bases'] = int(newvalue)

    elif param == 'phred_Qscore_offset':
        assert isinstance(int(newvalue), int), \
            "phred_Qscore_offset must be an integer."
        self.paramsdict['phred_Qscore_offset'] = int(newvalue)

    elif param == 'mindepth_statistical':
        assert isinstance(int(newvalue), int), \
            "mindepth_statistical must be an integer."
        ## do not allow values below 5
        if int(newvalue) < 5:
            raise IPyradError("""
    mindepth statistical cannot be set < 5. Use mindepth_majrule.""")
        else:
            self.paramsdict['mindepth_statistical'] = int(newvalue)

    elif param == 'mindepth_majrule':
        assert isinstance(int(newvalue), int), \
            "mindepth_majrule must be an integer."
        self.paramsdict['mindepth_majrule'] = int(newvalue)

    elif param == 'maxdepth':
        self.paramsdict['maxdepth'] = int(newvalue)

    elif param == 'clust_threshold':
        newvalue = float(newvalue)
        assert (newvalue < 1) & (newvalue > 0), \
        "clust_threshold must be a decimal value between 0 and 1."
        self.paramsdict['clust_threshold'] = newvalue

    elif param == 'max_barcode_mismatch':
        self.paramsdict['max_barcode_mismatch'] = int(newvalue)

    elif param == 'filter_adapters':
        self.paramsdict['filter_adapters'] = int(newvalue)

    elif param == 'filter_min_trim_len':
        self.paramsdict["filter_min_trim_len"] = int(newvalue)

    elif param == 'max_alleles_consens':
        self.paramsdict['max_alleles_consens'] = int(newvalue)

    elif param == 'max_Ns_consens':
        newvalue = _tuplecheck(newvalue, int)
        assert isinstance(newvalue, tuple), \
        "max_Ns_consens should be a tuple e.g., (8, 8)"
        self.paramsdict['max_Ns_consens'] = newvalue

    elif param == 'max_Hs_consens':
        newvalue = _tuplecheck(newvalue, int)
        assert isinstance(newvalue, tuple), \
        "max_Hs_consens should be a tuple e.g., (5, 5)"
        self.paramsdict['max_Hs_consens'] = newvalue

    elif param == 'min_samples_locus':
        self.paramsdict['min_samples_locus'] = int(newvalue)

    elif param == 'max_shared_Hs_locus':
        if isinstance(newvalue, str):
            if newvalue.isdigit():
                newvalue = int(newvalue)
            else:
                try:
                    newvalue = float(newvalue)
                except Exception as inst:
                    raise IPyradParamsError("""
    max_shared_Hs_locus must be int or float, you put: {}""".format(newvalue))
        self.paramsdict['max_shared_Hs_locus'] = newvalue

    elif param == 'max_SNPs_locus':
        newvalue = _tuplecheck(newvalue, int)
        assert isinstance(newvalue, tuple), \
        "max_SNPs_locus should be a tuple e.g., (20, 20)"
        self.paramsdict['max_SNPs_locus'] = newvalue

    elif param == 'max_Indels_locus':
        newvalue = _tuplecheck(newvalue, int)
        assert isinstance(newvalue, tuple), \
        "max_Indels_locus should be a tuple e.g., (5, 100)"
        self.paramsdict['max_Indels_locus'] = newvalue

    ## deprecated but retained for legacy, now uses trim_reads (below)
    elif param == 'edit_cutsites':
        ## Force into a string tuple
        newvalue = _tuplecheck(newvalue)
        ## try converting each tup element to ints
        newvalue = list(newvalue)
        for i in range(2):
            try:
                newvalue[i] = int(newvalue[i])
            except (ValueError, IndexError):
                newvalue.append(0)
                pass
        newvalue = tuple(newvalue)
        ## make sure we have a nice tuple
        if not isinstance(newvalue, tuple):
            raise IPyradWarningExit("""
    Error: edit_cutsites should be a tuple e.g., (0, 5) or ('TGCAG', 6),
    you entered {}
    """.format(newvalue))
        self.paramsdict['edit_cutsites'] = newvalue

    elif param == 'trim_reads':
        ## Force into a string tuple
        newvalue = _tuplecheck(newvalue)
        ## try converting each tup element to ints
        newvalue = list(newvalue)
        for i in range(4):
            try:
                newvalue[i] = int(newvalue[i])
            except (ValueError, IndexError):
                newvalue.append(0)
                pass
        newvalue = tuple(newvalue)
        ## make sure we have a nice tuple
        if not isinstance(newvalue, tuple):
            raise IPyradWarningExit("""
    Error: trim_reads should be a tuple e.g., (0, -5, -5, 0) 
    or (0, 90, 0, 90), or (0, 0, 0, 0). 
    You entered {}\n""".format(newvalue))
        self.paramsdict['trim_reads'] = newvalue        

    ## deprecated but retained for legacy, now named trim_loci 
    elif param == 'trim_overhang':
        newvalue = _tuplecheck(newvalue, str)
        assert isinstance(newvalue, tuple), \
        "trim_overhang should be a tuple e.g., (4, *, *, 4)"
        self.paramsdict['trim_overhang'] = tuple([int(i) for i in newvalue])

    elif param == 'trim_loci':
        newvalue = _tuplecheck(newvalue, str)
        assert isinstance(newvalue, tuple), \
        "trim_overhang should be a tuple e.g., (0, -5, -5, 0)"
        self.paramsdict['trim_loci'] = tuple([int(i) for i in newvalue])


    elif param == 'output_formats':
        ## let's get whatever the user entered as a tuple of letters
        allowed = assemble.write_outfiles.OUTPUT_FORMATS.keys()

        #<<<<<<< HEAD
        ## Handle the case where output formats is an empty string
        if isinstance(newvalue, str):
            ## strip commas and spaces from string so we have only letters
            newvalue = newvalue.replace(",", "").replace(" ", "")
            newvalue = list(newvalue)
            if not newvalue:
                newvalue = ["*"]
        if isinstance(newvalue, tuple):
            newvalue = list(newvalue)
        #=======
        #if isinstance(newvalue, tuple):
        #    newvalue = list(newvalue)
        #if isinstance(newvalue, str):
        #    newvalue = [i.strip() for i in newvalue.split(",")]
        #    ## Handle the case where output formats is empty
        #    if not any(newvalue):
        #        newvalue = "*"
        #>>>>>>> 488144d1d97240b8b6f6caf9cfb6c023bb6ebb36
        if isinstance(newvalue, list):
            ## if more than letters, raise an warning
            if any([len(i) > 1 for i in newvalue]):
                LOGGER.warning("""
    'output_formats' params entry is malformed. Setting to * to avoid errors.""")
                newvalue = allowed
            newvalue = tuple(newvalue)
            #newvalue = tuple([i for i in newvalue if i in allowed])
        if "*" in newvalue:
            newvalue = allowed

        ## set the param
        self.paramsdict['output_formats'] = newvalue


    elif param == 'pop_assign_file':
        fullpoppath = _expander(newvalue)

        ## if a path is entered, raise exception if not found
        if newvalue:
            if not os.path.isfile(fullpoppath):
                LOGGER.warn("Population assignment file not found.")
                raise IPyradWarningExit("""
    Warning: Population assignment file not found. This must be an
    absolute path (/home/wat/ipyrad/data/my_popfile.txt) or relative to
    the directory where you're running ipyrad (./data/my_popfile.txt)
    You entered: {}\n""".format(fullpoppath))
        ## should we add a check here that all pop samples are in samples?

            self.paramsdict['pop_assign_file'] = fullpoppath
            self._link_populations()
        else:
            self.paramsdict['pop_assign_file'] = ""
            ## Don't forget to possibly blank the populations dictionary
            self.populations = {}

    return self