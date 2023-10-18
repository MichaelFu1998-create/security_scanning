def parse_single_results(data, sample, res1):
    """ parse results from cutadapt into sample data"""

    ## set default values 
    #sample.stats_dfs.s2["reads_raw"] = 0
    sample.stats_dfs.s2["trim_adapter_bp_read1"] = 0
    sample.stats_dfs.s2["trim_quality_bp_read1"] = 0
    sample.stats_dfs.s2["reads_filtered_by_Ns"] = 0
    sample.stats_dfs.s2["reads_filtered_by_minlen"] = 0
    sample.stats_dfs.s2["reads_passed_filter"] = 0

    ## parse new values from cutadapt results output
    lines = res1.strip().split("\n")
    for line in lines:

        if "Total reads processed:" in line:
            value = int(line.split()[3].replace(",", ""))
            sample.stats_dfs.s2["reads_raw"] = value

        if "Reads with adapters:" in line:
            value = int(line.split()[3].replace(",", ""))
            sample.stats_dfs.s2["trim_adapter_bp_read1"] = value

        if "Quality-trimmed" in line:
            value = int(line.split()[1].replace(",", ""))
            sample.stats_dfs.s2["trim_quality_bp_read1"] = value

        if "Reads that were too short" in line:
            value = int(line.split()[5].replace(",", ""))
            sample.stats_dfs.s2["reads_filtered_by_minlen"] = value

        if "Reads with too many N" in line:
            value = int(line.split()[5].replace(",", ""))
            sample.stats_dfs.s2["reads_filtered_by_Ns"] = value
   
        if "Reads written (passing filters):" in line:
            value = int(line.split()[4].replace(",", ""))
            sample.stats_dfs.s2["reads_passed_filter"] = value

    ## save to stats summary
    if sample.stats_dfs.s2.reads_passed_filter:
        sample.stats.state = 2
        sample.stats.reads_passed_filter = sample.stats_dfs.s2.reads_passed_filter
        sample.files.edits = [
            (OPJ(data.dirs.edits, sample.name+".trimmed_R1_.fastq.gz"), 0)]
        ## write the long form output to the log file.
        LOGGER.info(res1)

    else:
        print("{}No reads passed filtering in Sample: {}".format(data._spacer, sample.name))