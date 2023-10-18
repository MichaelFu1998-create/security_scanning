def data_cleanup(data):
    """ cleanup / statswriting function for Assembly obj """
    data.stats_dfs.s3 = data._build_stat("s3")
    data.stats_files.s3 = os.path.join(data.dirs.clusts, "s3_cluster_stats.txt")
    with io.open(data.stats_files.s3, 'w') as outfile:
        data.stats_dfs.s3.to_string(
            buf=outfile,
            formatters={
                'merged_pairs':'{:.0f}'.format,
                'clusters_total':'{:.0f}'.format,
                'clusters_hidepth':'{:.0f}'.format,
                'filtered_bad_align':'{:.0f}'.format,
                'avg_depth_stat':'{:.2f}'.format,
                'avg_depth_mj':'{:.2f}'.format,
                'avg_depth_total':'{:.2f}'.format,
                'sd_depth_stat':'{:.2f}'.format,
                'sd_depth_mj':'{:.2f}'.format,
                'sd_depth_total':'{:.2f}'.format
            })