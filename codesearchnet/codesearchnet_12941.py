def parse_pair_results(data, sample, res):
    """ parse results from cutadapt for paired data"""
    LOGGER.info("in parse pair mod results\n%s", res)   
    ## set default values
    sample.stats_dfs.s2["trim_adapter_bp_read1"] = 0
    sample.stats_dfs.s2["trim_adapter_bp_read2"] = 0    
    sample.stats_dfs.s2["trim_quality_bp_read1"] = 0
    sample.stats_dfs.s2["trim_quality_bp_read2"] = 0    
    sample.stats_dfs.s2["reads_filtered_by_Ns"] = 0
    sample.stats_dfs.s2["reads_filtered_by_minlen"] = 0
    sample.stats_dfs.s2["reads_passed_filter"] = 0

    lines = res.strip().split("\n")
    qprimed = 0
    for line in lines:
        ## set primer to catch next line
        if "Quality-trimmed" in line:
            qprimed = 1

        ## grab read1 and read2 lines when qprimed
        if "Read 1:" in line:
            if qprimed:
                value = int(line.split()[2].replace(",", ""))
                sample.stats_dfs.s2["trim_quality_bp_read1"] = value

        if "Read 2:" in line:
            if qprimed:
                value = int(line.split()[2].replace(",", ""))
                sample.stats_dfs.s2["trim_quality_bp_read2"] = value
                qprimed = 0

        if "Read 1 with adapter:" in line:
            value = int(line.split()[4].replace(",", ""))
            sample.stats_dfs.s2["trim_adapter_bp_read1"] = value

        if "Read 2 with adapter:" in line:
            value = int(line.split()[4].replace(",", ""))
            sample.stats_dfs.s2["trim_adapter_bp_read2"] = value

        if "Total read pairs processed:" in line:
            value = int(line.split()[4].replace(",", ""))
            sample.stats_dfs.s2["reads_raw"] = value

        if "Pairs that were too short" in line:
            value = int(line.split()[5].replace(",", ""))
            sample.stats_dfs.s2["reads_filtered_by_minlen"] = value

        if "Pairs with too many N" in line:
            value = int(line.split()[5].replace(",", ""))
            sample.stats_dfs.s2["reads_filtered_by_Ns"] = value

        if "Pairs written (passing filters):" in line:
            value = int(line.split()[4].replace(",", ""))
            sample.stats_dfs.s2["reads_passed_filter"] = value

    ## save to stats summary
    if sample.stats_dfs.s2.reads_passed_filter:
        sample.stats.state = 2
        sample.stats.reads_passed_filter = sample.stats_dfs.s2.reads_passed_filter
        sample.files.edits = [(
             OPJ(data.dirs.edits, sample.name+".trimmed_R1_.fastq.gz"), 
             OPJ(data.dirs.edits, sample.name+".trimmed_R2_.fastq.gz")
             )]

    else:
        print("No reads passed filtering in Sample: {}".format(sample.name))