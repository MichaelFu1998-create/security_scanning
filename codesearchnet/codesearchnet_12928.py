def dask_chroms(data, samples):
    """
    A dask relay function to fill chroms for all samples
    """
    
    ## example concatenating with dask
    h5s = [os.path.join(data.dirs.across, s.name+".tmp.h5") for s in samples]
    handles = [h5py.File(i) for i in h5s]
    dsets = [i['/ichrom'] for i in handles]
    arrays = [da.from_array(dset, chunks=(10000, 3)) for dset in dsets]
    stack = da.stack(arrays, axis=2)

    ## max chrom (should we check for variable hits? if so, things can get wonk)
    maxchrom = da.max(stack, axis=2)[:, 0]

    ## max pos
    maxpos = da.max(stack, axis=2)[:, 2]

    ## min pos
    mask = stack == 0
    stack[mask] = 9223372036854775807  ## max int64 value
    minpos = da.min(stack, axis=2)[:, 1]
    final = da.stack([maxchrom, minpos, maxpos], axis=1)
    final.to_hdf5(data.clust_database, "/chroms")

    ## close the h5 handles
    _ = [i.close() for i in handles]