def scaffolds_to_contigs(infile, outfile, number_contigs=False):
    '''Makes a file of contigs from scaffolds by splitting at every N.
       Use number_contigs=True to add .1, .2, etc onto end of each
       contig, instead of default to append coordinates.'''
    seq_reader = sequences.file_reader(infile)
    fout = utils.open_file_write(outfile)

    for seq in seq_reader:
        contigs = seq.contig_coords()
        counter = 1
        for contig in contigs:
            if number_contigs:
                name = seq.id + '.' + str(counter)
                counter += 1
            else:
                name = '.'.join([seq.id, str(contig.start + 1), str(contig.end + 1)])
            print(sequences.Fasta(name, seq[contig.start:contig.end+1]), file=fout)

    utils.close(fout)