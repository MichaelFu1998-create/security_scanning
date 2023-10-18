def fastq_touchup_for_vsearch_merge(read, outfile, reverse=False):
    """ option to change orientation of reads and sets Qscore to B """
    
    counts = 0
    with open(outfile, 'w') as out:
        ## read in paired end read files 4 lines at a time
        if read.endswith(".gz"):
            fr1 = gzip.open(read, 'rb')
        else:
            fr1 = open(read, 'rb')
        quarts = itertools.izip(*[iter(fr1)]*4)

        ## a list to store until writing
        writing = []

        while 1:
            try:
                lines = quarts.next()
            except StopIteration:
                break
            if reverse:
                seq = lines[1].strip()[::-1]
            else:
                seq = lines[1].strip()
            writing.append("".join([
                lines[0],
                seq+"\n",
                lines[2],
                "B"*len(seq)
            ]))

            ## write to disk
            counts += 1
            if not counts % 1000:
                out.write("\n".join(writing)+"\n")
                writing = []
        if writing:
            out.write("\n".join(writing))
            
    out.close()
    fr1.close()