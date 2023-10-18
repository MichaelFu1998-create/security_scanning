def interleave(infile_1, infile_2, outfile, suffix1=None, suffix2=None):
    '''Makes interleaved file from two sequence files. If used, will append suffix1 onto end
    of every sequence name in infile_1, unless it already ends with suffix1. Similar for sufffix2.'''
    seq_reader_1 = sequences.file_reader(infile_1)
    seq_reader_2 = sequences.file_reader(infile_2)
    f_out = utils.open_file_write(outfile)

    for seq_1 in seq_reader_1:
        try:
            seq_2 = next(seq_reader_2)
        except:
            utils.close(f_out)
            raise Error('Error getting mate for sequence', seq_1.id, ' ... cannot continue')

        if suffix1 is not None and not seq_1.id.endswith(suffix1):
            seq_1.id += suffix1
        if suffix2 is not None and not seq_2.id.endswith(suffix2):
            seq_2.id += suffix2

        print(seq_1, file=f_out)
        print(seq_2, file=f_out)

    try:
        seq_2 = next(seq_reader_2)
    except:
        seq_2 = None

    if seq_2 is not None:
        utils.close(f_out)
        raise Error('Error getting mate for sequence', seq_2.id, ' ... cannot continue')

    utils.close(f_out)