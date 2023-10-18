def mapreads(data, sample, nthreads, force):
    """ 
    Attempt to map reads to reference sequence. This reads in the fasta files
    (samples.files.edits), and maps each read to the reference. Unmapped reads 
    are dropped right back in the de novo pipeline. Reads that map successfully
    are processed and pushed downstream and joined with the rest of the data 
    post muscle_align. 

    Mapped reads end up in a sam file.
    """

    LOGGER.info("Entering mapreads(): %s %s", sample.name, nthreads)

    ## This is the input derep file, for paired data we need to split the data, 
    ## and so we will make sample.files.dereps == [derep1, derep2], but for 
    ## SE data we can simply use sample.files.derep == [derepfile].
    derepfile = os.path.join(data.dirs.edits, sample.name+"_derep.fastq")
    sample.files.dereps = [derepfile]

    ## This is the final output files containing merged/concat derep'd refmap'd 
    ## reads that did not match to the reference. They will be back in 
    ## merge/concat (--nnnnn--) format ready to be input to vsearch, if needed. 
    mumapfile = sample.files.unmapped_reads
    umap1file = os.path.join(data.dirs.edits, sample.name+"-tmp-umap1.fastq")
    umap2file = os.path.join(data.dirs.edits, sample.name+"-tmp-umap2.fastq")        

    ## split the derepfile into the two handles we designate
    if "pair" in data.paramsdict["datatype"]:
        sample.files.split1 = os.path.join(data.dirs.edits, sample.name+"-split1.fastq")
        sample.files.split2 = os.path.join(data.dirs.edits, sample.name+"-split2.fastq")
        sample.files.dereps = [sample.files.split1, sample.files.split2]
        split_merged_reads(sample.files.dereps, derepfile)

    ## (cmd1) smalt <task> [TASK_OPTIONS] [<index_name> <file_name_A> [<file_name_B>]]
    ##  -f sam       : Output as sam format, tried :clip: to hard mask output 
    ##                 but it shreds the unmapped reads (outputs empty fq)
    ##  -l [pe,mp,pp]: If paired end select the orientation of each read
    ##  -n #         : Number of threads to use
    ##  -x           : Perform a more exhaustive search
    ##  -y #         : proportion matched to reference (sequence similarity)
    ##  -o           : output file
    ##               : Reference sequence
    ##               : Input file(s), in a list. One for R1 and one for R2
    ##  -c #         : proportion of the query read length that must be covered

    ## (cmd1) bwa mem [OPTIONS] <index_name> <file_name_A> [<file_name_B>] > <output_file>
    ##  -t #         : Number of threads
    ##  -M           : Mark split alignments as secondary.

    ## (cmd2) samtools view [options] <in.bam>|<in.sam>|<in.cram> [region ...] 
    ##   -b = write to .bam
    ##   -q = Only keep reads with mapq score >= 30 (seems to be pretty standard)
    ##   -F = Select all reads that DON'T have these flags. 
    ##         0x4 (segment unmapped)
    ##         0x100 (Secondary alignment)
    ##         0x800 (supplementary alignment)
    ##   -U = Write out all reads that don't pass the -F filter 
    ##        (all unmapped reads go to this file).

    ## TODO: Should eventually add `-q 13` to filter low confidence mapping.
    ## If you do this it will throw away some fraction of reads. Ideally you'd
    ## catch these and throw them in with the rest of the unmapped reads, but
    ## I can't think of a straightforward way of doing that. There should be 
    ## a `-Q` flag to only keep reads below the threshold, but i realize that
    ## would be of limited use besides for me.

    ## (cmd3) samtools sort [options...] [in.bam]
    ##   -T = Temporary file name, this is required by samtools, ignore it
    ##        Here we hack it to be samhandle.tmp cuz samtools cleans it up
    ##   -O = Output file format, in this case bam
    ##   -o = Output file name

    if "smalt" in data._hackersonly["aligner"]:
        ## The output SAM data is written to file (-o)
        ## input is either (derep) or (derep-split1, derep-split2)
        cmd1 = [ipyrad.bins.smalt, "map", 
                "-f", "sam", 
                "-n", str(max(1, nthreads)),
                "-y", str(data.paramsdict['clust_threshold']), 
                "-o", os.path.join(data.dirs.refmapping, sample.name+".sam"),
                "-x",
                data.paramsdict['reference_sequence']
                ] + sample.files.dereps
        cmd1_stdout = sps.PIPE
        cmd1_stderr = sps.STDOUT
    else:
        cmd1 = [ipyrad.bins.bwa, "mem",
                "-t", str(max(1, nthreads)),
                "-M",
                data.paramsdict['reference_sequence']
                ] + sample.files.dereps
        ## Insert optional flags for bwa
        try:
            bwa_args = data._hackersonly["bwa_args"].split()
            bwa_args.reverse()
            for arg in bwa_args:
                cmd1.insert(2, arg)
        except KeyError:
            ## Do nothing
            pass
        cmd1_stdout = open(os.path.join(data.dirs.refmapping, sample.name+".sam"), 'w')
        cmd1_stderr = None

    ## Reads in the SAM file from cmd1. It writes the unmapped data to file
    ## and it pipes the mapped data to be used in cmd3
    cmd2 = [ipyrad.bins.samtools, "view", 
           "-b", 
           ## TODO: This introduces a bug with PE right now. Think about the case where
           ## R1 has low qual mapping and R2 has high. You get different numbers
           ## of reads in the unmapped tmp files. FML.
           #"-q", "30",
           "-F", "0x904",
           "-U", os.path.join(data.dirs.refmapping, sample.name+"-unmapped.bam"), 
           os.path.join(data.dirs.refmapping, sample.name+".sam")]

    ## this is gonna catch mapped bam output from cmd2 and write to file
    cmd3 = [ipyrad.bins.samtools, "sort", 
            "-T", os.path.join(data.dirs.refmapping, sample.name+".sam.tmp"),
            "-O", "bam", 
            "-o", sample.files.mapped_reads]

    ## TODO: Unnecessary?
    ## this is gonna read the sorted BAM file and index it. only for pileup?
    cmd4 = [ipyrad.bins.samtools, "index", sample.files.mapped_reads]

    ## this is gonna read in the unmapped files, args are added below, 
    ## and it will output fastq formatted unmapped reads for merging.
    ## -v 45 sets the default qscore arbitrarily high
    cmd5 = [ipyrad.bins.samtools, "bam2fq", "-v 45",
            os.path.join(data.dirs.refmapping, sample.name+"-unmapped.bam")]

    ## Insert additional arguments for paired data to the commands.
    ## We assume Illumina paired end reads for the orientation 
    ## of mate pairs (orientation: ---> <----). 
    if 'pair' in data.paramsdict["datatype"]:
        if "smalt" in data._hackersonly["aligner"]:
            ## add paired flag (-l pe) to cmd1 right after (smalt map ...)
            cmd1.insert(2, "pe")
            cmd1.insert(2, "-l")
        else:
            ## No special PE flags for bwa
            pass
        ## add samtools filter for only keep if both pairs hit
        ## 0x1 - Read is paired
        ## 0x2 - Each read properly aligned
        cmd2.insert(2, "0x3")
        cmd2.insert(2, "-f")

        ## tell bam2fq that there are output files for each read pair
        cmd5.insert(2, umap1file)
        cmd5.insert(2, "-1")
        cmd5.insert(2, umap2file)
        cmd5.insert(2, "-2")
    else:
        cmd5.insert(2, mumapfile)
        cmd5.insert(2, "-0")

    ## Running cmd1 creates ref_mapping/sname.sam, 
    LOGGER.debug(" ".join(cmd1))
    proc1 = sps.Popen(cmd1, stderr=cmd1_stderr, stdout=cmd1_stdout)

    ## This is really long running job so we wrap it to ensure it dies. 
    try:
        error1 = proc1.communicate()[0]
    except KeyboardInterrupt:
        proc1.kill()

    ## raise error if one occurred in smalt
    if proc1.returncode:
        raise IPyradWarningExit(error1)

    ## Running cmd2 writes to ref_mapping/sname.unmapped.bam, and 
    ## fills the pipe with mapped BAM data
    LOGGER.debug(" ".join(cmd2))
    proc2 = sps.Popen(cmd2, stderr=sps.STDOUT, stdout=sps.PIPE)

    ## Running cmd3 pulls mapped BAM from pipe and writes to 
    ## ref_mapping/sname.mapped-sorted.bam. 
    ## Because proc2 pipes to proc3 we just communicate this to run both.
    LOGGER.debug(" ".join(cmd3))
    proc3 = sps.Popen(cmd3, stderr=sps.STDOUT, stdout=sps.PIPE, stdin=proc2.stdout)
    error3 = proc3.communicate()[0]
    if proc3.returncode:
        raise IPyradWarningExit(error3)
    proc2.stdout.close()

    ## Later we're gonna use samtools to grab out regions using 'view', and to
    ## do that we need it to be indexed. Let's index it now. 
    LOGGER.debug(" ".join(cmd4))
    proc4 = sps.Popen(cmd4, stderr=sps.STDOUT, stdout=sps.PIPE)
    error4 = proc4.communicate()[0]
    if proc4.returncode:
        raise IPyradWarningExit(error4)
    
    ## Running cmd5 writes to either edits/sname-refmap_derep.fastq for SE
    ## or it makes edits/sname-tmp-umap{12}.fastq for paired data, which 
    ## will then need to be merged.
    LOGGER.debug(" ".join(cmd5))
    proc5 = sps.Popen(cmd5, stderr=sps.STDOUT, stdout=sps.PIPE)
    error5 = proc5.communicate()[0]
    if proc5.returncode:
        raise IPyradWarningExit(error5)

    ## Finally, merge the unmapped reads, which is what cluster()
    ## expects. If SE, just rename the outfile. In the end
    ## <sample>-refmap_derep.fq will be the final output
    if 'pair' in data.paramsdict["datatype"]:
        LOGGER.info("Merging unmapped reads {} {}".format(umap1file, umap2file))
        merge_pairs_after_refmapping(data, [(umap1file, umap2file)], mumapfile)