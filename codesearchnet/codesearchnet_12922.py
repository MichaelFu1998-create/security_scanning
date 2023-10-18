def get_nloci(data):
    """ return nloci from the tmp h5 arr"""
    bseeds = os.path.join(data.dirs.across, data.name+".tmparrs.h5")
    with h5py.File(bseeds) as io5:
        return io5["seedsarr"].shape[0]