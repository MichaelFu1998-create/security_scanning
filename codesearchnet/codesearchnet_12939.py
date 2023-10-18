def assembly_cleanup(data):
    """ cleanup for assembly object """

    ## build s2 results data frame
    data.stats_dfs.s2 = data._build_stat("s2")
    data.stats_files.s2 = os.path.join(data.dirs.edits, 's2_rawedit_stats.txt')

    ## write stats for all samples
    with io.open(data.stats_files.s2, 'w', encoding='utf-8') as outfile:
        data.stats_dfs.s2.fillna(value=0).astype(np.int).to_string(outfile)