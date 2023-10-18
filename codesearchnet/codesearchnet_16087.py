def count_sequences(infile):
    '''Returns the number of sequences in a file'''
    seq_reader = sequences.file_reader(infile)
    n = 0
    for seq in seq_reader:
        n += 1
    return n