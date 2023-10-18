def _cleanup_and_die(data):
    """ cleanup func for step 1 """
    tmpfiles = glob.glob(os.path.join(data.dirs.fastqs, "tmp_*_R*.fastq"))
    tmpfiles += glob.glob(os.path.join(data.dirs.fastqs, "tmp_*.p"))
    for tmpf in tmpfiles:            
        os.remove(tmpf)