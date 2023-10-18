def choose_samples(samples, force):
    """ filter out samples that are already done with this step, unless force"""

    ## hold samples that pass
    subsamples = []
    ## filter the samples again
    if not force:
        for sample in samples:
            if sample.stats.state >= 2:
                print("""\
    Skipping Sample {}; Already filtered. Use force argument to overwrite.\
    """.format(sample.name))
            elif not sample.stats.reads_raw:
                print("""\
    Skipping Sample {}; No reads found in file {}\
    """.format(sample.name, sample.files.fastqs))
            else:
                subsamples.append(sample)

    else:
        for sample in samples:
            if not sample.stats.reads_raw:
                print("""\
    Skipping Sample {}; No reads found in file {}\
    """.format(sample.name, sample.files.fastqs))
            else:
                subsamples.append(sample)
    return subsamples