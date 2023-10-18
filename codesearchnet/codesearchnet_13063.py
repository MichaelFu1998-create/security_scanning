def make(data, samples):
    """ reads in .loci and builds alleles from case characters """
    
    #read in loci file
    outfile = open(os.path.join(data.dirs.outfiles, data.name+".alleles"), 'w')
    lines = open(os.path.join(data.dirs.outfiles, data.name+".loci"), 'r')

    ## Get the longest sample name for pretty printing
    longname = max(len(x) for x in data.samples.keys())

    ## Padding between name and sequence in output file. This should be the 
    ## same as write_outfiles.write_tmp_loci.name_padding
    name_padding = 5
    writing = []
    loc = 0
    for line in lines:
        if ">" in line:
            name, seq = line.split(" ")[0], line.split(" ")[-1]
            allele1, allele2 = splitalleles(seq.strip())

            ## Format the output string. the "-2" below accounts for the additional
            ## 2 characters added to the sample name that don't get added to the
            ## snpsites line, so you gotta bump this line back 2 to make it
            ## line up right.
            writing.append(name+"_0"+" "*(longname-len(name)-2+name_padding)+allele1)
            writing.append(name+"_1"+" "*(longname-len(name)-2+name_padding)+allele2)
        else:
            writing.append(line.strip())
        loc += 1

        ## print every 10K loci "
        if not loc % 10000:
            outfile.write("\n".join(writing)+"\n")
            writing = []

    outfile.write("\n".join(writing))
    outfile.close()