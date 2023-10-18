def merge_to_one_seq(infile, outfile, seqname='union'):
    '''Takes a multi fasta or fastq file and writes a new file that contains just one sequence, with the original sequences catted together, preserving their order'''
    seq_reader = sequences.file_reader(infile)
    seqs = []

    for seq in seq_reader:
        seqs.append(copy.copy(seq))

    new_seq = ''.join([seq.seq for seq in seqs])

    if type(seqs[0]) == sequences.Fastq:
        new_qual = ''.join([seq.qual for seq in seqs])
        seqs[:] = []
        merged = sequences.Fastq(seqname, new_seq, new_qual)
    else:
        merged = sequences.Fasta(seqname, new_seq)
        seqs[:] = []

    f = utils.open_file_write(outfile)
    print(merged, file=f)
    utils.close(f)