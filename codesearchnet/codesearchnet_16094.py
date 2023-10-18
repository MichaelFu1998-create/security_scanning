def sort_by_name(infile, outfile):
    '''Sorts input sequence file by sort -d -k1,1, writes sorted output file.'''
    seqs = {}
    file_to_dict(infile, seqs)
    #seqs = list(seqs.values())
    #seqs.sort()
    fout = utils.open_file_write(outfile)
    for name in sorted(seqs):
        print(seqs[name], file=fout)
    utils.close(fout)