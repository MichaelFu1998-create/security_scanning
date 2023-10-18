def to_fastg(infile, outfile, circular=None):
    '''Writes a FASTG file in SPAdes format from input file. Currently only whether or not a sequence is circular is supported. Put circular=set of ids, or circular=filename to make those sequences circular in the output. Puts coverage=1 on all contigs'''
    if circular is None:
        to_circularise = set()
    elif type(circular) is not set:
        f = utils.open_file_read(circular)
        to_circularise = set([x.rstrip() for x in f.readlines()])
        utils.close(f)
    else:
        to_circularise = circular

    seq_reader = sequences.file_reader(infile)
    fout = utils.open_file_write(outfile)
    nodes = 1

    for seq in seq_reader:
        new_id = '_'.join([
            'NODE', str(nodes),
            'length', str(len(seq)),
            'cov', '1',
            'ID', seq.id
        ])

        if seq.id in to_circularise:
            seq.id = new_id + ':' + new_id + ';'
            print(seq, file=fout)
            seq.revcomp()
            seq.id = new_id + "':" + new_id + "';"
            print(seq, file=fout)
        else:
            seq.id = new_id + ';'
            print(seq, file=fout)
            seq.revcomp()
            seq.id = new_id + "';"
            print(seq, file=fout)

        nodes += 1

    utils.close(fout)