def cleanup_tempfiles(data):
    """ 
    Function to remove older files. This is called either in substep 1 or after
    the final substep so that tempfiles are retained for restarting interrupted
    jobs until we're sure they're no longer needed. 
    """

    ## remove align-related tmp files
    tmps1 = glob.glob(os.path.join(data.tmpdir, "*.fa"))
    tmps2 = glob.glob(os.path.join(data.tmpdir, "*.npy"))
    for tmp in tmps1 + tmps2:
        if os.path.exists(tmp):
            os.remove(tmp)

    ## remove cluster related files
    removal = [
        os.path.join(data.dirs.across, data.name+".utemp"),
        os.path.join(data.dirs.across, data.name+".htemp"),
        os.path.join(data.dirs.across, data.name+"_catcons.tmp"),
        os.path.join(data.dirs.across, data.name+"_cathaps.tmp"),
        os.path.join(data.dirs.across, data.name+"_catshuf.tmp"),
        os.path.join(data.dirs.across, data.name+"_catsort.tmp"),
        os.path.join(data.dirs.across, data.name+".tmparrs.h5"),
        os.path.join(data.dirs.across, data.name+".tmp.indels.hdf5"),
        ]
    for rfile in removal:
        if os.path.exists(rfile):
            os.remove(rfile)

    ## remove singlecat related h5 files
    smpios = glob.glob(os.path.join(data.dirs.across, '*.tmp.h5'))
    for smpio in smpios:
        if os.path.exists(smpio):
            os.remove(smpio)