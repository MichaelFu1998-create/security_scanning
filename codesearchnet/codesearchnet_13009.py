def write_gphocs(data, sidx):
    """
    write the g-phocs output. This code is hella ugly bcz it's copy/pasted
    directly from the old loci2gphocs script from pyrad. I figure having it
    get done the stupid way is better than not having it done at all, at
    least for the time being. This could probably be sped up significantly.
    """

    outfile = data.outfiles.gphocs
    infile = data.outfiles.loci

    infile = open(infile)
    outfile = open(outfile, 'w')

    ## parse the loci
    ## Each set of reads at a locus is appended with a line
    ## beginning with // and ending with |x, where x in the locus id.
    ## so after this call 'loci' will contain an array
    ## of sets of each read per locus.
    loci = re.compile("\|[0-9]+\|").split(infile.read())[:-1]

    # Print the header, the number of loci in this file
    outfile.write(str(len(loci)) + "\n\n")

    # iterate through each locus, print out the header for each locus:
    # <locus_name> <n_samples> <locus_length>
    # Then print the data for each sample in this format:
    # <individual_name> <sequence>
    for i, loc in enumerate(loci):
        ## Get rid of the line that contains the snp info
        loc = loc.rsplit("\n", 1)[0]

        # Separate out each sequence within the loc block. 'sequences'
        # will now be a list strings containing name/sequence pairs.
        # We select each line in the locus string that starts with ">"
        names = [line.split()[0] for line in loc.strip().split("\n")]
        try:
            sequences = [line.split()[1] for line in loc.strip().split("\n")]
        except:
            pass
        # Strips off 'nnnn' separator for paired data
        # replaces '-' with 'N'
        editsequences = [seq.replace("n","").replace('-','N') for seq in sequences]
        sequence_length = len(editsequences[0])

        # get length of longest name and add 4 spaces
        longname = max(map(len,names))+4

        # Print out the header for this locus
        outfile.write('locus{} {} {}\n'.format(str(i), len(sequences), sequence_length))

        # Iterate through each sequence read at this locus and write it to the file.
        for name,sequence in zip(names, editsequences):
            # Clean up the sequence data to make gphocs happy. Only accepts UPPER
            # case chars for bases, and only accepts 'N' for missing data.
            outfile.write(name+" "*(longname-len(name))+sequence + "\n")
        ## Separate loci with so it's prettier
        outfile.write("\n")