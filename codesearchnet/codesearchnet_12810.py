def sample_cleanup(data, sample):
    """
    Clean up a bunch of loose files.
    """
    umap1file = os.path.join(data.dirs.edits, sample.name+"-tmp-umap1.fastq")
    umap2file = os.path.join(data.dirs.edits, sample.name+"-tmp-umap2.fastq")
    unmapped = os.path.join(data.dirs.refmapping, sample.name+"-unmapped.bam")
    samplesam = os.path.join(data.dirs.refmapping, sample.name+".sam")
    split1 = os.path.join(data.dirs.edits, sample.name+"-split1.fastq")
    split2 = os.path.join(data.dirs.edits, sample.name+"-split2.fastq")
    refmap_derep = os.path.join(data.dirs.edits, sample.name+"-refmap_derep.fastq")
    for f in [umap1file, umap2file, unmapped, samplesam, split1, split2, refmap_derep]:
        try:
            os.remove(f)
        except:
            pass