def _read_sample_names(fname):
    """ Read in sample names from a plain text file. This is a convenience
    function for branching so if you have tons of sample names you can
    pass in a file rather than having to set all the names at the command
    line.
    """
    try:
        with open(fname, 'r') as infile:
            subsamples = [x.split()[0] for x in infile.readlines() if x.strip()]

    except Exception as inst:
        print("Failed to read input file with sample names.\n{}".format(inst))
        raise inst

    return subsamples