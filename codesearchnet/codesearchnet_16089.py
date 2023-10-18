def make_random_contigs(contigs, length, outfile, name_by_letters=False, prefix='', seed=None, first_number=1):
    '''Makes a multi fasta file of random sequences, all the same length'''
    random.seed(a=seed)
    fout = utils.open_file_write(outfile)
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    letters_index = 0

    for i in range(contigs):
        if name_by_letters:
            name = letters[letters_index]
            letters_index += 1
            if letters_index == len(letters):
                letters_index = 0
        else:
            name = str(i + first_number)

        fa = sequences.Fasta(prefix + name, ''.join([random.choice('ACGT') for x in range(length)]))
        print(fa, file=fout)

    utils.close(fout)