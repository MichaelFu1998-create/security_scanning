def split_by_base_count(infile, outfiles_prefix, max_bases, max_seqs=None):
    '''Splits a fasta/q file into separate files, file size determined by number of bases.

    Puts <= max_bases in each split file The exception is a single sequence >=max_bases
    is put in its own file.  This does not split sequences.
    '''
    seq_reader = sequences.file_reader(infile)
    base_count = 0
    file_count = 1
    seq_count = 0
    fout = None
    if max_seqs is None:
        max_seqs = float('inf')

    for seq in seq_reader:
        if base_count == 0:
            fout = utils.open_file_write(outfiles_prefix + '.' + str(file_count))
            file_count += 1

        if base_count + len(seq) > max_bases or seq_count >= max_seqs:
            if base_count == 0:
                print(seq, file=fout)
                utils.close(fout)
            else:
                utils.close(fout)
                fout = utils.open_file_write(outfiles_prefix + '.' + str(file_count))
                print(seq, file=fout)
                base_count = len(seq)
                file_count += 1
                seq_count = 1
        else:
            base_count += len(seq)
            seq_count += 1
            print(seq, file=fout)

    utils.close(fout)