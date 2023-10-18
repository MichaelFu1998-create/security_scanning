def file_reader(fname, read_quals=False):
    '''Iterates over a FASTA or FASTQ file, yielding the next sequence in the file until there are no more sequences'''
    f = utils.open_file_read(fname)
    line = f.readline()
    phylip_regex = re.compile('^\s*[0-9]+\s+[0-9]+$')
    gbk_regex = re.compile('^LOCUS\s+\S')

    if line.startswith('>'):
        seq = Fasta()
        previous_lines[f] = line
    elif line.startswith('##gff-version 3'):
        seq = Fasta()
        # if a GFF file, need to skip past all the annotation
        # and get to the fasta sequences at the end of the file
        while not line.startswith('>'):
            line = f.readline()
            if not line:
                utils.close(f)
                raise Error('No sequences found in GFF file "' + fname + '"')

        seq = Fasta()
        previous_lines[f] = line
    elif line.startswith('ID   ') and line[5] != ' ':
        seq = Embl()
        previous_lines[f] = line
    elif gbk_regex.search(line):
        seq = Embl()
        previous_lines[f] = line
    elif line.startswith('@'):
        seq = Fastq()
        previous_lines[f] = line
    elif phylip_regex.search(line):
        # phylip format could be interleaved or not, need to look at next
        # couple of lines to figure that out. Don't expect these files to
        # be too huge, so just store all the sequences in memory
        number_of_seqs, bases_per_seq = line.strip().split()
        number_of_seqs = int(number_of_seqs)
        bases_per_seq = int(bases_per_seq)
        got_blank_line = False

        first_line = line
        seq_lines = []
        while 1:
            line = f.readline()
            if line == '':
                break
            elif line == '\n':
                got_blank_line = True
            else:
                seq_lines.append(line.rstrip())
        utils.close(f)

        if len(seq_lines) == 1 or len(seq_lines) == number_of_seqs:
            sequential = True
        elif seq_lines[0][10] != ' ' and seq_lines[1][10] == ' ':
            sequential = True
        else:
            sequential = False

        # if the 11th char of second sequence line is a space,  then the file is sequential, e.g.:
        # GAGCCCGGGC AATACAGGGT AT
        # as opposed to:
        # Salmo gairAAGCCTTGGC AGTGCAGGGT
        if sequential:
            current_id = None
            current_seq = ''
            for line in seq_lines:
                if len(current_seq) == bases_per_seq or len(current_seq) == 0:
                    if current_id is not None:
                        yield Fasta(current_id, current_seq.replace('-', ''))
                    current_seq = ''
                    current_id, new_bases = line[0:10].rstrip(), line.rstrip()[10:]
                else:
                    new_bases = line.rstrip()

                current_seq += new_bases.replace(' ','')

            yield Fasta(current_id, current_seq.replace('-', ''))
        else:
            # seaview files start all seqs at pos >=12. Other files start
            # their sequence at the start of the line
            if seq_lines[number_of_seqs + 1][0] == ' ':
                first_gap_pos = seq_lines[0].find(' ')
                end_of_gap = first_gap_pos
                while seq_lines[0][end_of_gap] == ' ':
                    end_of_gap += 1
                first_seq_base = end_of_gap
            else:
                first_seq_base = 10

            seqs = []
            for i in range(number_of_seqs):
                name, bases = seq_lines[i][0:first_seq_base].rstrip(), seq_lines[i][first_seq_base:]
                seqs.append(Fasta(name, bases))

            for i in range(number_of_seqs, len(seq_lines)):
                seqs[i%number_of_seqs].seq += seq_lines[i]

            for fa in seqs:
                fa.seq = fa.seq.replace(' ','').replace('-','')
                yield fa

        return
    elif line == '':
        utils.close(f)
        return
    else:
        utils.close(f)
        raise Error('Error determining file type from file "' + fname + '". First line is:\n' + line.rstrip())

    try:
        while seq.get_next_from_file(f, read_quals):
            yield seq
    finally:
        utils.close(f)