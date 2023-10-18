def merge_after_pysam(data, clust):
    """
    This is for pysam post-flight merging. The input is a cluster
    for an individual locus. We have to split the clusters, write
    R1 and R2 to files then call merge_pairs(). This is not ideal,
    it's slow, but it works. This is the absolute worst way to do this,
    it bounces all the files for each locus off the disk. I/O _hog_.
    """
    try:
        r1file = tempfile.NamedTemporaryFile(mode='wb', delete=False,
                                            dir=data.dirs.edits,
                                            suffix="_R1_.fastq")
        r2file = tempfile.NamedTemporaryFile(mode='wb', delete=False,
                                            dir=data.dirs.edits,
                                            suffix="_R2_.fastq")

        r1dat = []
        r2dat = []
        for locus in clust:
            sname, seq = locus.split("\n")
            ## Have to munge the sname to make it look like fastq format
            sname = "@" + sname[1:]
            r1, r2 = seq.split("nnnn")
            r1dat.append("{}\n{}\n{}\n{}".format(sname, r1, "+", "B"*(len(r1))))
            r2dat.append("{}\n{}\n{}\n{}".format(sname, r2, "+", "B"*(len(r2))))

        r1file.write("\n".join(r1dat))
        r2file.write("\n".join(r2dat))
        r1file.close()
        r2file.close()

        ## Read in the merged data and format to return as a clust
        merged_file = tempfile.NamedTemporaryFile(mode='wb',
                                            dir=data.dirs.edits,
                                            suffix="_merged.fastq").name

        clust = []
        merge_pairs(data, [(r1file.name, r2file.name)], merged_file, 0, 1)

        with open(merged_file) as infile:
            quarts = itertools.izip(*[iter(infile)]*4)

            while 1:
                try:
                    sname, seq, _, _ = quarts.next()
                    ## Vsearch expects R2 oriented how it would be in a raw data file
                    ## i.e. revcomp, and that's also how it returns it
                    ## but we want to maintain the genomic orientation so R1 and
                    ## R2 are both on the + strand and both in ascending positional order
                    ## so here if the reads don't merge we have to revcomp R2
                    if not "_m1" in sname.rsplit(";", 1)[1]:
                        try:
                            R1, R2 = seq.split("nnnn")
                            seq = R1 + "nnnn" + revcomp(R2)
                        except ValueError as inst:
                            LOGGER.error("Failed merge_after_pysam: {} {}".format(sname, seq))
                            raise

                except StopIteration:
                    break
                ## put sname back
                sname = ">" + sname[1:]
                clust.extend([sname.strip(), seq.strip()])
    except:
        LOGGER.info("Error in merge_pairs post-refmap.")
        raise
    finally:
        for i in [r1file.name, r2file.name, merged_file]:
            if os.path.exists(i):
                log_level = logging.getLevelName(LOGGER.getEffectiveLevel())
                ## uncomment this to shit ALL over the filesystem. 
                ## if not log_level == "DEBUG":
                os.remove(i)

    return clust