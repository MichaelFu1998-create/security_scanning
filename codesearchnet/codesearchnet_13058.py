def get_subsamples(data, samples, force):
    """
    Apply state, ncluster, and force filters to select samples to be run.
    """

    subsamples = []
    for sample in samples:
        if not force:
            if sample.stats.state >= 5:
                print("""\
    Skipping Sample {}; Already has consens reads. Use force arg to overwrite.\
    """.format(sample.name))
            elif not sample.stats.clusters_hidepth:
                print("""\
    Skipping Sample {}; No clusters found."""\
    .format(sample.name, int(sample.stats.clusters_hidepth)))
            elif sample.stats.state < 4:
                print("""\
    Skipping Sample {}; not yet finished step4 """\
    .format(sample.name))
            else:
                subsamples.append(sample)

        else:
            if not sample.stats.clusters_hidepth:
                print("""\
    Skipping Sample {}; No clusters found in {}."""\
    .format(sample.name, sample.files.clusters))
            elif sample.stats.state < 4:
                print("""\
    Skipping Sample {}; not yet finished step4"""\
    .format(sample.name))
            else:
                subsamples.append(sample)

    if len(subsamples) == 0:
        raise IPyradWarningExit("""
    No samples to cluster, exiting.
    """)

    ## if sample is already done skip
    if "hetero_est" not in data.stats:
        print("  No estimates of heterozygosity and error rate. Using default "\
              "values")
        for sample in subsamples:
            sample.stats.hetero_est = 0.001
            sample.stats.error_est = 0.0001

    if data._headers:
        print(u"""\
  Mean error  [{:.5f} sd={:.5f}]
  Mean hetero [{:.5f} sd={:.5f}]"""\
  .format(data.stats.error_est.mean(), data.stats.error_est.std(),
          data.stats.hetero_est.mean(), data.stats.hetero_est.std()))

    return subsamples