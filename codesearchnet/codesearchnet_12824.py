def refmap_init(data, sample, force):
    """ create some file handles for refmapping """
    ## make some persistent file handles for the refmap reads files
    sample.files.unmapped_reads = os.path.join(data.dirs.edits, 
                                  "{}-refmap_derep.fastq".format(sample.name))
    sample.files.mapped_reads = os.path.join(data.dirs.refmapping,
                                  "{}-mapped-sorted.bam".format(sample.name))