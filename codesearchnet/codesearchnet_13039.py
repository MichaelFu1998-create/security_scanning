def reconcat(data, sample):
    """ takes aligned chunks (usually 10) and concatenates them """

    try:
        ## get chunks
        chunks = glob.glob(os.path.join(data.tmpdir,
                 sample.name+"_chunk_[0-9].aligned"))

        ## sort by chunk number, cuts off last 8 =(aligned)
        chunks.sort(key=lambda x: int(x.rsplit("_", 1)[-1][:-8]))
        LOGGER.info("chunk %s", chunks)
        ## concatenate finished reads
        sample.files.clusters = os.path.join(data.dirs.clusts,
                                             sample.name+".clustS.gz")
        ## reconcats aligned clusters
        with gzip.open(sample.files.clusters, 'wb') as out:
            for fname in chunks:
                with open(fname) as infile:
                    dat = infile.read()
                    ## avoids mess if last chunk was empty
                    if dat.endswith("\n"):
                        out.write(dat+"//\n//\n")
                    else:
                        out.write(dat+"\n//\n//\n")
                os.remove(fname)
    except Exception as inst:
        LOGGER.error("Error in reconcat {}".format(inst))
        raise