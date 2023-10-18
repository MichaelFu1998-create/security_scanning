def load_PSFLab_file(fname):
    """Load the array `data` in the .mat file `fname`."""
    if os.path.exists(fname) or os.path.exists(fname + '.mat'):
        return loadmat(fname)['data']
    else:
        raise IOError("Can't find PSF file '%s'" % fname)