def to_boulderio(infile, outfile):
    '''Converts input sequence file into a "Boulder-IO format", as used by primer3'''
    seq_reader = sequences.file_reader(infile)
    f_out = utils.open_file_write(outfile)

    for sequence in seq_reader:
        print("SEQUENCE_ID=" + sequence.id, file=f_out)
        print("SEQUENCE_TEMPLATE=" + sequence.seq, file=f_out)
        print("=", file=f_out)

    utils.close(f_out)