def declone_3rad(data, sample):
    """
    3rad uses random adapters to identify pcr duplicates. We will
    remove pcr dupes here. Basically append the radom adapter to
    each sequence, do a regular old vsearch derep, then trim
    off the adapter, and push it down the pipeline. This will
    remove all identical seqs with identical random i5 adapters.
    """

    LOGGER.info("Entering declone_3rad - {}".format(sample.name))

    ## Append i5 adapter to the head of each read. Merged file is input, and
    ## still has fq qual score so also have to append several qscores for the
    ## adapter bases. Open the merge file, get quarts, go through each read
    ## and append the necessary stuff.

    adapter_seqs_file = tempfile.NamedTemporaryFile(mode='wb',
                                        delete=False,
                                        dir=data.dirs.edits,
                                        suffix="_append_adapters_.fastq")

    try:
        with open(sample.files.edits[0][0]) as infile:
            quarts = itertools.izip(*[iter(infile)]*4)

            ## a list to store until writing
            writing = []
            counts = 0

            while 1:
                try:
                    read = quarts.next()
                except StopIteration:
                    break

                ## Split on +, get [1], split on "_" (can be either _r1 or
                ## _m1 if merged reads) and get [0] for the i5
                ## prepend "EEEEEEEE" as qscore for the adapters
                i5 = read[0].split("+")[1].split("_")[0]

                ## If any non ACGT in the i5 then drop this sequence
                if 'N' in i5:
                    continue
                writing.append("\n".join([
                                read[0].strip(),
                                i5 + read[1].strip(),
                                read[2].strip(),
                                "E"*8 + read[3].strip()]
                            ))

                ## Write the data in chunks
                counts += 1
                if not counts % 1000:
                    adapter_seqs_file.write("\n".join(writing)+"\n")
                    writing = []
            if writing:
                adapter_seqs_file.write("\n".join(writing))
                adapter_seqs_file.close()

        tmp_outfile = tempfile.NamedTemporaryFile(mode='wb',
                                        delete=False,
                                        dir=data.dirs.edits,
                                        suffix="_decloned_w_adapters_.fastq")

        ## Close the tmp file bcz vsearch will write to it by name, then
        ## we will want to reopen it to read from it.
        tmp_outfile.close()
        ## Derep the data (adapters+seq)
        derep_and_sort(data, adapter_seqs_file.name,
                       os.path.join(data.dirs.edits, tmp_outfile.name), 2)

        ## Remove adapters from head of sequence and write out
        ## tmp_outfile is now the input file for the next step
        ## first vsearch derep discards the qscore so we iterate
        ## by pairs
        with open(tmp_outfile.name) as infile:
            with open(os.path.join(data.dirs.edits, sample.name+"_declone.fastq"),\
                                'wb') as outfile:
                duo = itertools.izip(*[iter(infile)]*2)

                ## a list to store until writing
                writing = []
                counts2 = 0

                while 1:
                    try:
                        read = duo.next()
                    except StopIteration:
                        break

                    ## Peel off the adapters. There's probably a faster
                    ## way of doing this.
                    writing.append("\n".join([
                                    read[0].strip(),
                                    read[1].strip()[8:]]
                                ))

                    ## Write the data in chunks
                    counts2 += 1
                    if not counts2 % 1000:
                        outfile.write("\n".join(writing)+"\n")
                        writing = []
                if writing:
                    outfile.write("\n".join(writing))
                    outfile.close()

        LOGGER.info("Removed pcr duplicates from {} - {}".format(sample.name, counts-counts2))

    except Exception as inst:
        raise IPyradError("    Caught error while decloning "\
                                + "3rad data - {}".format(inst))

    finally:
        ## failed samples will cause tmp file removal to raise.
        ## just ignore it.
        try:
            ## Clean up temp files
            if os.path.exists(adapter_seqs_file.name):
                os.remove(adapter_seqs_file.name)
            if os.path.exists(tmp_outfile.name):
                os.remove(tmp_outfile.name)
        except Exception as inst:
            pass