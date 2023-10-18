def setup_dirs(data):
    """ sets up directories for step3 data """
    ## make output folder for clusters
    pdir = os.path.realpath(data.paramsdict["project_dir"])
    data.dirs.clusts = os.path.join(pdir, "{}_clust_{}"\
                       .format(data.name, data.paramsdict["clust_threshold"]))
    if not os.path.exists(data.dirs.clusts):
        os.mkdir(data.dirs.clusts)

    ## make a tmpdir for align files
    data.tmpdir = os.path.abspath(os.path.expanduser(
        os.path.join(pdir, data.name+'-tmpalign')))
    if not os.path.exists(data.tmpdir):
        os.mkdir(data.tmpdir)

    ## If ref mapping, init samples and make the refmapping output directory.
    if not data.paramsdict["assembly_method"] == "denovo":
        ## make output directory for read mapping process
        data.dirs.refmapping = os.path.join(pdir, "{}_refmapping".format(data.name))
        if not os.path.exists(data.dirs.refmapping):
            os.mkdir(data.dirs.refmapping)