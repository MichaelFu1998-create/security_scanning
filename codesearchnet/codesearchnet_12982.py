def run(data, samples, force, ipyclient):
    """
    Check all samples requested have been clustered (state=6), make output
    directory, then create the requested outfiles. Excluded samples are already
    removed from samples.
    """

    ## prepare dirs
    data.dirs.outfiles = os.path.join(data.dirs.project, data.name+"_outfiles")
    if not os.path.exists(data.dirs.outfiles):
        os.mkdir(data.dirs.outfiles)

    ## make the snps/filters data base, fills the dups and inds filters
    ## and fills the splits locations
    data.database = os.path.join(data.dirs.outfiles, data.name+".hdf5")
    init_arrays(data)

    ## Apply filters to supercatg and superhdf5 with selected samples
    ## and fill the filters and edge arrays.
    filter_all_clusters(data, samples, ipyclient)

    ## Everything needed is in the now filled h5 database. Filters were applied
    ## with 'samples' taken into account. Now we create the loci file (default)
    ## output and build a stats file.
    data.outfiles.loci = os.path.join(data.dirs.outfiles, data.name+".loci")
    data.outfiles.alleles = os.path.join(data.dirs.outfiles, data.name+".alleles.loci")
    make_loci_and_stats(data, samples, ipyclient)

    ## OPTIONAL OUTPUTS:
    output_formats = data.paramsdict["output_formats"]

    ## held separate from *output_formats cuz it's big and parallelized
    if any([x in output_formats for x in ["v", "V"]]):
        full = "V" in output_formats
        try:
            make_vcf(data, samples, ipyclient, full=full)
        except IPyradWarningExit as inst:
            ## Something fsck vcf build. Sometimes this is simply a memory
            ## issue, so trap the exception and allow it to try building
            ## the other output formats.
            print("  Error building vcf. See ipyrad_log.txt for details.")
            LOGGER.error(inst)

    ## make other array-based formats, recalcs keeps and arrays
    make_outfiles(data, samples, output_formats, ipyclient)

    ## print friendly message
    shortpath = data.dirs.outfiles.replace(os.path.expanduser("~"), "~")
    print("{}Outfiles written to: {}\n".format(data._spacer, shortpath))