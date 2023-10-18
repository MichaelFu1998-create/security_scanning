def split_merged_reads(outhandles, input_derep):
    """
    Takes merged/concat derep file from vsearch derep and split it back into 
    separate R1 and R2 parts. 
    - sample_fastq: a list of the two file paths to write out to.
    - input_reads: the path to the input merged reads
    """

    handle1, handle2 = outhandles
    splitderep1 = open(handle1, 'w')
    splitderep2 = open(handle2, 'w')

    with open(input_derep, 'r') as infile: 
        ## Read in the infile two lines at a time: (seqname, sequence)
        duo = itertools.izip(*[iter(infile)]*2)

        ## lists for storing results until ready to write
        split1s = []
        split2s = []

        ## iterate over input splitting, saving, and writing.
        idx = 0
        while 1:
            try:
                itera = duo.next()
            except StopIteration:
                break
            ## split the duo into separate parts and inc counter
            part1, part2 = itera[1].split("nnnn")
            idx += 1

            ## R1 needs a newline, but R2 inherits it from the original file            
            ## store parts in lists until ready to write
            split1s.append("{}{}\n".format(itera[0], part1))
            split2s.append("{}{}".format(itera[0], part2))

            ## if large enough then write to file
            if not idx % 10000:
                splitderep1.write("".join(split1s))
                splitderep2.write("".join(split2s))
                split1s = []
                split2s = [] 

    ## write final chunk if there is any
    if any(split1s):
        splitderep1.write("".join(split1s))
        splitderep2.write("".join(split2s))

    ## close handles
    splitderep1.close()
    splitderep2.close()