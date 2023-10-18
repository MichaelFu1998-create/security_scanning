def acgtn_only(infile, outfile):
    '''Replace every non-acgtn (case insensitve) character with an N'''
    f = utils.open_file_write(outfile)
    for seq in sequences.file_reader(infile):
        seq.replace_non_acgt()
        print(seq, file=f)
    utils.close(f)