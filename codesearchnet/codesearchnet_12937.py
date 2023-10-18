def run(data, samples, noreverse, force, randomseed, ipyclient, **kwargs):
    """
    For step 6 the run function is sub divided a bit so that users with really
    difficult assemblies can possibly interrupt and restart the step from a 
    checkpoint. 

    Substeps that are run:
     1. build concat consens file, 
     2. cluster all consens,
     3. split clusters into bits,
     4. align bits, 
     5. build indel array
     6. build h5 array.
     7. Enter seq data & cleanup
    """

    ## if force then set checkpoint to zero and run all substeps for just
    ## the user specified steps. 
    if force:
        data._checkpoint = 0
        if kwargs.get('substeps'):
            substeps = kwargs.get('substeps')
        else:  
            substeps = range(1, 8)

    ## if {data}._checkpoint attribute exists then find the checkpoint where
    ## this assembly left off (unless force) and build step list from there.
    else:
        if kwargs.get('substeps'):
            substeps = kwargs.get('substeps')
        else:  
            if hasattr(data, '_checkpoint'):
                substeps = range(max(1, data._checkpoint), 8)
            else:
                data._checkpoint = 0
                substeps = range(1, 8)

    ## build substeps list to subset which funtions need to be run
    if isinstance(substeps, (int, float, str)):
        substeps = [substeps]
        substeps = [int(i) for i in substeps]

    ## print continuation message
    if substeps[0] != 1:
        print("{}Continuing from checkpoint 6.{}"\
              .format(data._spacer, substeps[0]))
    LOGGER.info("checkpoint = %s", data._checkpoint)
    LOGGER.info("substeps = %s", substeps)

    ## Set variables on data that are needed for all steps;
    data.dirs.across = os.path.realpath(
        os.path.join(data.paramsdict["project_dir"], data.name+"_across"))
    data.tmpdir = os.path.join(data.dirs.across, data.name+"-tmpalign")
    data.clust_database = os.path.join(data.dirs.across, data.name+".clust.hdf5")
    if not os.path.exists(data.dirs.across):
        os.mkdir(data.dirs.across)
    if not os.path.exists(data.tmpdir):
        os.mkdir(data.tmpdir)
    data.cpus = data._ipcluster["cores"]
    if not data.cpus:
        data.cpus = len(ipyclient)

    ## STEP 6-1: Clean database and build input concat file for clustering
    if 1 in substeps:
        clean_and_build_concat(data, samples, randomseed, ipyclient)
        data._checkpoint = 1

    ## STEP 6-2: Cluster across w/ vsearch; uses all threads on largest host 
    if 2 in substeps:
        call_cluster(data, noreverse, ipyclient)
        data._checkpoint = 2

    ## builds consens cluster bits and writes them to the tmp directory. These
    ## will not be deleted until either step 6-6 is complete, or the force flag
    ## is used. This will clear the tmpdir if it is run.
    if 3 in substeps:
        build_clustbits(data, ipyclient, force)
        data._checkpoint = 3

    ## muscle align the cluster bits and create tmp hdf5 indel arrays for the
    ## next step. These will not be deleted until...
    if 4 in substeps:
        multi_muscle_align(data, samples, ipyclient)
        data._checkpoint = 4

    ## fill the indel array with the indel tmp arrays from aligning step.
    if 5 in substeps:
        build_indels(data, samples, ipyclient)
        data._checkpoint = 5

    if 6 in substeps:
        ## builds the final HDF5 array which includes three main keys
        ## /catg -- contains all indiv catgs and has indels inserted
        ##   .attr['samples'] = [samples]
        ## /filters -- filled for dups, left empty for others until step 7.
        ##   .attr['filters'] = [f1, f2, f3, f4, f5]
        ## /seqs -- contains the clustered sequence data as string arrays
        ##   .attr['samples'] = [samples]
        ## /edges -- gets the paired split locations for now.
        ## /snps  -- left empty for now

        ## FILL SUPERCATG and fills dupfilter, indfilter, and nalleles
        ## this function calls singlecat() on each sample and enters their
        ## resulting arrays into the superarray. If all singlecats are built
        ## then it will continue to enter them into the database. 
        LOGGER.info("multicat -- building full database")
        new_multicat(data, samples, ipyclient)
        data._checkpoint = 6

    if 7 in substeps:
        ## FILL SUPERSEQS and fills edges(splits) for paired-end data
        fill_superseqs(data, samples)
        data._checkpoint = 7

        ## remove files but not dir (used in step 1 too)
        cleanup_tempfiles(data)
        ## remove the tmpdir
        if os.path.exists(data.tmpdir):
            shutil.rmtree(data.tmpdir)

        ## set sample states
        for sample in samples:
            sample.stats.state = 6
        print("")