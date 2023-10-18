def bam_region_to_fasta(data, sample, proc1, chrom, region_start, region_end):
    """ 
    Take the chromosome position, and start and end bases and return sequences
    of all reads that overlap these sites. This is the command we're building:

    samtools view -b 1A_sorted.bam 1:116202035-116202060 | \
             samtools bam2fq <options> -

            -b      : output bam format
            -0      : For SE, output all reads to this file
            -1/-2   : For PE, output first and second reads to different files
            -       : Tell samtools to read in from the pipe

    Write out the sam output and parse it to return as fasta for clust.gz file. 
    We also grab the reference sequence with a @REF header to aid in alignment
    for single-end data. This will be removed post-alignment. 
    """

    ## output bam file handle for storing genome regions
    bamf = sample.files.mapped_reads
    if not os.path.exists(bamf):
        raise IPyradWarningExit("  file not found - %s", bamf)

    # chrom = re.escape(repr(chrom))[1:-1].replace('\\\\', '\\')
    #LOGGER.info("before: %s", chrom)
    chrom.replace("|", r"\|")
    chrom.replace("(", r"\(")
    chrom.replace(")", r"\)")
    #LOGGER.info("after: %s", chrom)

    ## What we want to do is have the num-chrom dict as an arg, then build this
    ## string as three ints [chrom-int, pos-start, pos-end]
    #cint = cdict[chrom]
    #cpstring = "__{}_{}_{}__".format(cint, int(region_start)+1, region_end)

    ## a string argument as input to commands, indexed at either 0 or 1, 
    ## and with pipe characters removed from chromo names
    ## rstring_id1 is for fetching the reference sequence bcz faidx is
    ## 1 indexed
    rstring_id1 = "{}:{}-{}"\
        .format(chrom, str(int(region_start)+1), region_end)

    ## rstring_id0 is just for printing out the reference CHROM/POS
    ## in the read name
    rstring_id0 = "{}:{}-{}"\
        .format(chrom, region_start, region_end)

    ## If SE then we enforce the minimum overlap distance to avoid the 
    ## staircase syndrome of multiple reads overlapping just a little.
    overlap_buffer = 0
    if not "pair" in data.paramsdict["datatype"]:
        overlap_buffer = data._hackersonly["min_SE_refmap_overlap"]

    ## rstring_id0_buffered is for samtools view. We have to play patty
    ## cake here with the two rstring_id0s because we want `view` to 
    ## enforce the buffer for SE, but we want the reference sequence
    ## start and end positions to print correctly for downstream.
    rstring_id0_buffered = "{}:{}-{}"\
        .format(chrom, int(region_start) + overlap_buffer,\
                int(region_end) - overlap_buffer)

    ## The "samtools faidx" command will grab this region from reference 
    ## which we'll paste in at the top of each stack to aid alignment.
    cmd1 = [ipyrad.bins.samtools, "faidx", 
            data.paramsdict["reference_sequence"], 
            rstring_id1, " ; echo __done__"]

    ## Call the command, I found that it doesn't work with shell=False if 
    ## the refstring is 'MT':100-200', but it works if it is MT:100-200. 
    LOGGER.info("Grabbing bam_region_to_fasta:\n {}".format(cmd1))
    #proc1 = sps.Popen(cmd1, stderr=sps.STDOUT, stdout=sps.PIPE)
    #ref = proc1.communicate()[0]
    #if proc1.returncode:
    #    raise IPyradWarningExit("  error in %s: %s", cmd1, ref)

    ## push the samtools faidx command to our subprocess, then accumulate
    ## the results from stdout
    print(" ".join(cmd1), file=proc1.stdin)
    ref = ""
    for line in iter(proc1.stdout.readline, "//\n"):
        if "__done__" in line:
            break
        ref += line

    ## initialize the fasta list.
    fasta = []

    ## parse sam to fasta. Save ref location to name.
    ## Set size= an improbably large value so the REF sequence
    ## sorts to the top for muscle aligning.
    try:
        name, seq = ref.strip().split("\n", 1)
        seq = "".join(seq.split("\n"))
        fasta = ["{}_REF;size={};+\n{}".format(name, 1000000, seq)]
    except ValueError as inst:
        LOGGER.error("ref failed to parse - {}".format(ref))
        LOGGER.error(" ".join(cmd1))

    ## if PE then you have to merge the reads here
    if "pair" in data.paramsdict["datatype"]:
        ## PE R1 can either be on the forward or the reverse strand.
        ## Samtools view always outputs reads with respect to the
        ## forward strand. This means that reads with R1 on reverse
        ## end up with the R1 and R2 reference sequences swapped
        ## in the clust.gz file. There is a way to fix it but it's
        ## very annoying and i'm not sure if it's worth it...
        ## Drop the reference sequence for now...
        ##
        ## If you ever fix this be sure to remove the reference sequence
        ## from each cluster post alignment in cluster_within/align_and_parse()
        fasta = []

        ## Create temporary files for R1, R2 and merged, which we will pass to
        ## the function merge_pairs() which calls vsearch to test merging.
        ##
        ## If you are on linux then creating the temp files in /dev/shm
        ## should improve performance
        if os.path.exists("/dev/shm"):
            prefix = os.path.join("/dev/shm",
                            "{}-{}".format(sample.name, rstring_id0))
        else:
            prefix = os.path.join(data.dirs.refmapping, 
                            "{}-{}".format(sample.name, rstring_id0))
        read1 = "{}-R1".format(prefix)
        read2 = "{}-R2".format(prefix)
        merged = "{}-merged".format(prefix)

        ## Grab all the reads that map to this genomic location and dump
        ## fastq to R1 and R2 files.
        ## `-v 45` sets the default qscore to something high
        cmd1 = " ".join([ipyrad.bins.samtools, "view", "-b", bamf, rstring_id0])
        cmd2 = " ".join([ipyrad.bins.samtools, "bam2fq", "-v", "45", "-1", read1, "-2", read2, "-", "; echo __done__"])
        cmd = " | ".join([cmd1, cmd2])

        print(cmd, file=proc1.stdin)
        for line in iter(proc1.stdout.readline, "//\n"):
            if "__done__" in line:
                break

        ## run commands, pipe 1 -> 2, then cleanup
        ## proc1 = sps.Popen(cmd1, stderr=sps.STDOUT, stdout=sps.PIPE)
        ## proc2 = sps.Popen(cmd2, stderr=sps.STDOUT, stdout=sps.PIPE, stdin=proc1.stdout)
        ## res = proc2.communicate()[0]
        ## if proc2.returncode:
        ##     raise IPyradWarningExit("error {}: {}".format(cmd2, res))
        ## proc1.stdout.close()

        ## merge the pairs. 0 means don't revcomp bcz samtools already
        ## did it for us. 1 means "actually merge".
        try:
            ## return number of merged reads, writes merged data to 'merged'
            ## we don't yet do anything with the returned number of merged 
            _ = merge_pairs(data, [(read1, read2)], merged, 0, 1)

            with open(merged, 'r') as infile:
                quatro = itertools.izip(*[iter(infile)]*4)
                while 1:
                    try:
                        bits = quatro.next()
                    except StopIteration:
                        break
                    ## TODO: figure out a real way to get orientation for PE
                    orient = "+"
                    fullfast = ">{a};{b};{c};{d}\n{e}".format(
                        a=bits[0].split(";")[0],
                        b=rstring_id1,
                        c=bits[0].split(";")[1], 
                        d=orient,
                        e=bits[1].strip())
                    #,e=bits[9])
                    fasta.append(fullfast)

                ## TODO: If you ever figure out a good way to get the reference
                ## sequence included w/ PE then this commented call is useful
                ## for trimming the reference sequence to be the right length.
                ## If doing PE and R1/R2 don't overlap then the reference sequence
                ## will be quite long and will cause indel hell during the 
                ## alignment stage. Here trim the reference sequence to the length
                ## of the merged reads.
                ## This is commented out because we aren't currently including the
                ## ref seq for PE alignment.
                #fasta = trim_reference_sequence(fasta)

        except (OSError, ValueError, IPyradError) as inst:
            ## ValueError raised inside merge_pairs() if it can't open one
            ## or both of the files. Write this out, but ignore for now.
            ## Failed merging, probably unequal number of reads in R1 and R2
            ## IPyradError raised if merge_pairs can't read either R1 or R2
            ## file.
            ## Skip this locus?
            LOGGER.debug("Failed to merge reads, continuing; %s", inst)
            LOGGER.error("cmd - {}".format(cmd))
            return ""
        finally:
            ## Only clean up the files if they exist otherwise it'll raise.
            if os.path.exists(merged):
                os.remove(merged)
            if os.path.exists(read1):
                os.remove(read1)
            if os.path.exists(read2):
                os.remove(read2)
       
    else:
        try:
            ## SE if faster than PE cuz it skips writing intermedidate files
            ## rstring_id0_buffered is going to enforce the required 
            ## min_SE_refmap_overlap on either end of this region.
            cmd2 = [ipyrad.bins.samtools, "view", bamf, rstring_id0_buffered]
            proc2 = sps.Popen(cmd2, stderr=sps.STDOUT, stdout=sps.PIPE)
    
            ## run and check outputs
            res = proc2.communicate()[0]
            if proc2.returncode:
                raise IPyradWarningExit("{} {}".format(cmd2, res))

            ## if the region string is malformated you'll get back a warning
            ## from samtools
            if "[main_samview]" in res:
                raise IPyradError("Bad reference region {}".format(rstring_id0_buffered))

            ## do not join seqs that
            for line in res.strip().split("\n"):
                bits = line.split("\t")

                ## Read in the 2nd field (FLAGS), convert to binary
                ## and test if the 7th bit is set which indicates revcomp
                orient = "+"
                if int('{0:012b}'.format(int(bits[1]))[7]):
                    orient = "-"
                    ## Don't actually revcomp the sequence because samtools
                    ## writes out reference sequence on the forward strand
                    ## as well as reverse strand hits from the bam file.
                    #bits[9] = revcomp(bits[9])

                ## Rip insert the mapping position between the seq label and
                ## the vsearch derep size.
                fullfast = ">{a};{b};{c};{d}\n{e}".format(
                    a=bits[0].split(";")[0],
                    b=rstring_id0,
                    c=bits[0].split(";")[1],
                    d=orient,
                    e=bits[9])
                fasta.append(fullfast)
        except IPyradError as inst:
            ## If the mapped fragment is too short then the you'll get
            ## regions that look like this: scaffold262:299039-299036
            ## Just carry on, it's not a big deal.
            LOGGER.debug("Got a bad region string: {}".format(inst))
            return ""
        except (OSError, ValueError, Exception) as inst:
            ## Once in a blue moon something fsck and it breaks the
            ## assembly. No reason to give up if .001% of reads fail
            ## so just skip this locus.
            LOGGER.error("Failed get reads at a locus, continuing; %s", inst)
            LOGGER.error("cmd - {}".format(cmd2))
            return ""

    return "\n".join(fasta)