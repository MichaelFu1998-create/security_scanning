def split_by_fixed_size_onefile(infile, outfile, chunk_size, tolerance, skip_if_all_Ns=False):
    '''Splits each sequence in infile into chunks of fixed size, last chunk can be up to
       (chunk_size + tolerance) in length'''
    seq_reader = sequences.file_reader(infile)
    f_out = utils.open_file_write(outfile)
    for seq in seq_reader:
        for i in range(0, len(seq), chunk_size):
            if i + chunk_size + tolerance >= len(seq):
                end = len(seq)
            else:
                end = i + chunk_size

            subseq = seq.subseq(i, end)
            if not (skip_if_all_Ns and subseq.is_all_Ns()):
                subseq.id += '.' + str(i+1) + '_' + str(end)
                print(subseq, file=f_out)

            if end == len(seq):
                break

    utils.close(f_out)