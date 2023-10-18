def sort_by_size(infile, outfile, smallest_first=False):
    '''Sorts input sequence file by biggest sequence first, writes sorted output file. Set smallest_first=True to have smallest first'''
    seqs = {}
    file_to_dict(infile, seqs)
    seqs = list(seqs.values())
    seqs.sort(key=lambda x: len(x), reverse=not smallest_first)
    fout = utils.open_file_write(outfile)
    for seq in seqs:
        print(seq, file=fout)
    utils.close(fout)