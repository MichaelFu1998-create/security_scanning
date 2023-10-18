def split_by_fixed_size(infile, outfiles_prefix, chunk_size, tolerance, skip_if_all_Ns=False):
    '''Splits  fasta/q file into separate files, with up to (chunk_size + tolerance) bases in each file'''
    file_count = 1
    coords = []
    small_sequences = []  # sequences shorter than chunk_size
    seq_reader = sequences.file_reader(infile)
    f_coords = utils.open_file_write(outfiles_prefix + '.coords')

    for seq in seq_reader:
        if skip_if_all_Ns and seq.is_all_Ns():
             continue
        if len(seq) < chunk_size:
            small_sequences.append(copy.copy(seq))
        elif len(seq) <= chunk_size + tolerance:
            f = utils.open_file_write(outfiles_prefix + '.' + str(file_count))
            print(seq, file=f)
            utils.close(f)
            file_count += 1
        else:
            # make list of chunk coords
            chunks = [(x,x+chunk_size) for x in range(0, len(seq), chunk_size)]
            if chunks[-1][1] - 1 > len(seq):
                chunks[-1] = (chunks[-1][0], len(seq))
            if len(chunks) > 1 and (chunks[-1][1] - chunks[-1][0]) <= tolerance:
                chunks[-2] = (chunks[-2][0], chunks[-1][1])
                chunks.pop()

            # write one output file per chunk
            offset = 0
            for chunk in chunks:
                if not(skip_if_all_Ns and seq.is_all_Ns(start=chunk[0], end=chunk[1]-1)):
                    f = utils.open_file_write(outfiles_prefix + '.' + str(file_count))
                    chunk_id = seq.id + ':' + str(chunk[0]+1) + '-' + str(chunk[1])
                    print(sequences.Fasta(chunk_id, seq[chunk[0]:chunk[1]]), file=f)
                    print(chunk_id, seq.id, offset, sep='\t', file=f_coords)
                    utils.close(f)
                    file_count += 1

                offset += chunk[1] - chunk[0]

    # write files of small sequences
    if len(small_sequences):
        f = utils.open_file_write(outfiles_prefix + '.' + str(file_count))
        file_count += 1
        base_count = 0
        for seq in small_sequences:
            if base_count > 0 and base_count + len(seq) > chunk_size + tolerance:
                utils.close(f)
                f = utils.open_file_write(outfiles_prefix + '.' + str(file_count))
                file_count += 1
                base_count = 0

            print(seq, file=f)
            base_count += len(seq)

        utils.close(f)