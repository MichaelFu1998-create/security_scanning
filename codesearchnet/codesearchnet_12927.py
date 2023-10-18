def write_to_fullarr(data, sample, sidx):
    """ writes arrays to h5 disk """

    ## enter ref data?
    #isref = 'reference' in data.paramsdict["assembly_method"]
    LOGGER.info("writing fullarr %s %s", sample.name, sidx)

    ## save big arrays to disk temporarily
    with h5py.File(data.clust_database, 'r+') as io5:
        ## open views into the arrays we plan to fill
        chunk = io5["catgs"].attrs["chunksize"][0]
        catg = io5["catgs"]
        nall = io5["nalleles"]

        ## adding an axis to newcatg makes it write about 1000X faster.
        smpio = os.path.join(data.dirs.across, sample.name+'.tmp.h5')
        with h5py.File(smpio) as indat:

            ## grab all of the data from this sample's arrays
            newcatg = indat["icatg"] #[:]
            onall = indat["inall"]   #[:]

            ## enter it into the full array one chunk at a time
            for cidx in xrange(0, catg.shape[0], chunk):
                end = cidx + chunk
                catg[cidx:end, sidx:sidx+1, :] = np.expand_dims(newcatg[cidx:end, :], axis=1)
                nall[:, sidx:sidx+1] = np.expand_dims(onall, axis=1)