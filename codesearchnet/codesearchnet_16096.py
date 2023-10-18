def length_offsets_from_fai(fai_file):
    '''Returns a dictionary of positions of the start of each sequence, as
       if all the sequences were catted into one sequence.
       eg if file has three sequences, seq1 10bp, seq2 30bp, seq3 20bp, then
       the output would be: {'seq1': 0, 'seq2': 10, 'seq3': 40}'''
    positions = {}
    total_length = 0
    f = utils.open_file_read(fai_file)

    for line in f:
        try:
            (name, length) = line.rstrip().split()[:2]
            length = int(length)
        except:
            raise Error('Error reading the following line of fai file ' + fai_file + '\n' + line)

        positions[name] = total_length
        total_length += length

    utils.close(f)
    return positions