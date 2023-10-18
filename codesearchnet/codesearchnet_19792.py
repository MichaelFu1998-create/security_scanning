def fasta_file_to_dict(fasta_file, id=True, header=False, seq=False):
    """Returns a dict from a fasta file and the number of sequences as the second return value.
    fasta_file can be a string path or a file object.
    The key of fasta_dict can be set using the keyword arguments and
    results in a combination of id, header, sequence, in that order. joined with '||'. (default: id)
    Duplicate keys are checked and a warning is logged if found.
    The value of fasta_dict is a python dict with 3 keys: header, id and seq

    Changelog:
    2014/11/17:
    * Added support for url escaped id
    """
    fasta_file_f = fasta_file
    if isinstance(fasta_file, str):
        fasta_file_f = open(fasta_file, 'rb')

    fasta_dict = OrderedDict()
    keys = ['id', 'header', 'seq']
    flags = dict([('id', id), ('header', header), ('seq', seq)])
    entry = dict([('id', ''), ('header', ''), ('seq', '')])
    count = 0
    line_num = 0

    for line in fasta_file_f:
        line = line.strip()
        if line and line[0] == '>':
            count += 1
            key = '||'.join([entry[i] for i in keys if flags[i]])
            if key: # key != ''
                if key in fasta_dict: # check for duplicate key
                    logger.warning('%s : Line %d : Duplicate %s [%s] : ID = [%s].', fasta_file_f.name, line_num, '||'.join([i for i in keys if flags[i]]), key[:25] + (key[25:] and '..'), entry['id'])
                entry['seq'] = ''.join(entry['seq'])
                fasta_dict[key] = entry
                # check for url escaped id
                if id:
                    unescaped_id = unquote(entry['id'])
                    if id != unescaped_id:
                        key = '||'.join([unescaped_id] + [entry[i] for i in keys if i != 'id' and flags[i]])
                        entry['unescaped_id'] = unescaped_id
                        fasta_dict[key] = entry
                entry = dict()
            entry['header'] = line
            entry['id'] = line.split()[0][1:]
            entry['seq'] = []
        else:
            entry['seq'].append(line.upper())
        line_num += 1

    if isinstance(fasta_file, str):
        fasta_file_f.close()

    key = '||'.join([entry[i] for i in keys if flags[i]])
    if key: # key != ''
        if key in fasta_dict:
            logger.warning('%s : Line %d : Duplicate %s [%s] : ID = [%s].', fasta_file_f.name, line_num, '||'.join([i for i in keys if flags[i]]), key[:25] + (key[25:] and '..'), entry['id'])
        entry['seq'] = ''.join(entry['seq'])
        fasta_dict[key] = entry
        # check for url escaped id
        if id:
            unescaped_id = unquote(entry['id'])
            if id != unescaped_id:
                key = '||'.join([unescaped_id] + [entry[i] for i in keys if i != 'id' and flags[i]])
                entry['unescaped_id'] = unescaped_id
                fasta_dict[key] = entry

    return fasta_dict, count