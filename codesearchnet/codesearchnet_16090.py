def mean_length(infile, limit=None):
    '''Returns the mean length of the sequences in the input file. By default uses all sequences. To limit to the first N sequences, use limit=N'''
    total = 0
    count = 0
    seq_reader = sequences.file_reader(infile)
    for seq in seq_reader:
        total += len(seq)
        count += 1
        if limit is not None and count >= limit:
            break

    assert count > 0
    return total / count